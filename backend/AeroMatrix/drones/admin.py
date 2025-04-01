from django.contrib import admin, messages
from django import forms
from django.utils.safestring import mark_safe
from drones.infrastructure.models import Drone, Matrix
from django.contrib.admin.models import LogEntry, CHANGE
from django.utils.encoding import force_str
from django.contrib.contenttypes.models import ContentType
from django.utils.html import format_html
import json
from import_export.admin import ExportMixin


# ------------------------- Drone Form -------------------------

class DroneAdminForm(forms.ModelForm):
    class Meta:
        model = Drone
        fields = ("name", "model", "x", "y", "orientation", "matrix")
        help_texts = {
            "x": "The X coordinate must be within the matrix limits.",
            "y": "The Y coordinate must be within the matrix limits.",
            "matrix": "Select the matrix where this drone operates.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.matrix:
            max_x = self.instance.matrix.max_x - 1
            max_y = self.instance.matrix.max_y - 1
        else:
            max_x = 100
            max_y = 100
        self.fields["x"].widget = forms.NumberInput(attrs={"min": 0, "max": max_x, "step": 1})
        self.fields["y"].widget = forms.NumberInput(attrs={"min": 0, "max": max_y, "step": 1})

    def clean(self):
        cleaned_data = super().clean()
        x, y, matrix = cleaned_data.get("x"), cleaned_data.get("y"), cleaned_data.get("matrix")
        if not matrix:
            self.add_error("matrix", "A matrix must be selected.")
        if x is not None and (x < 0 or x >= matrix.max_x):
            self.add_error("x", f"The X coordinate must be between 0 and {matrix.max_x - 1}")
        if y is not None and (y < 0 or y >= matrix.max_y):
            self.add_error("y", f"The Y coordinate must be between 0 and {matrix.max_y - 1}")
        if x is not None and y is not None and matrix:
            exists = Drone.objects.filter(matrix=matrix, x=x, y=y).exclude(id=self.instance.id).exists()
            if exists:
                self.add_error(None, f"Another drone is already at ({x}, {y}) in this matrix.")
        return cleaned_data


# ------------------------- Drone Inline -------------------------

class DroneInlineForm(forms.ModelForm):
    class Meta:
        model = Drone
        fields = ("name", "model", "x", "y", "orientation", "matrix")

    def clean(self):
        cleaned_data = super().clean()
        x, y, matrix = cleaned_data.get("x"), cleaned_data.get("y"), self.instance.matrix
        if x is not None and (x < 0 or x >= matrix.max_x):
            self.add_error("x", f"X must be between 0 and {matrix.max_x - 1}")
        if y is not None and (y < 0 or y >= matrix.max_y):
            self.add_error("y", f"Y must be between 0 and {matrix.max_y - 1}")
        if x is not None and y is not None:
            exists = Drone.objects.filter(matrix=matrix, x=x, y=y).exclude(id=self.instance.id).exists()
            if exists:
                self.add_error(None, f"Another drone is at ({x}, {y}) in this matrix.")
        return cleaned_data


class DroneInline(admin.TabularInline):
    model = Drone
    form = DroneInlineForm
    extra = 1
    fields = ("name", "model", "x", "y", "orientation")
    show_change_link = True


# ------------------------- Drone Admin -------------------------

@admin.action(description="Reset selected drones to (0, 0)")
def reset_position(modeladmin, request, queryset):
    queryset.update(x=0, y=0)
    messages.success(request, "Selected drones reset to position (0, 0).")


@admin.register(Drone)
class DroneAdmin(admin.ModelAdmin):
    form = DroneAdminForm
    list_display = ("id", "name", "model", "current_position", "orientation_icon", "matrix")
    list_editable = ("matrix",)
    search_fields = ("name", "model")
    list_filter = ("orientation", "matrix")
    readonly_fields = ("id",)
    autocomplete_fields = ("matrix",)
    actions = [reset_position]

    fieldsets = (
        ("Identification", {"fields": ("name", "model")}),
        ("Position", {"fields": ("x", "y", "orientation", "matrix")}),
    )

    def current_position(self, obj):
        return format_html(
            '<span style="color: #555;">({},{})</span>', obj.x, obj.y
        )
    current_position.short_description = "Pos"

    def orientation_icon(self, obj):
        icons = {
            "N": "↑", "S": "↓", "E": "→", "O": "←"
        }
        return format_html(
            '<span style="font-size: 1.2rem;">{}</span>',
            icons.get(obj.orientation, "❓")
        )
    orientation_icon.short_description = "Direction"

    def save_model(self, request, obj, form, change):
        existing = Drone.objects.filter(matrix=obj.matrix, x=obj.x, y=obj.y).exclude(id=obj.id)
        if existing.exists():
            messages.error(request, f"❌ Position ({obj.x}, {obj.y}) already occupied.")
            return
        super().save_model(request, obj, form, change)
        messages.success(request, f"✅ Drone '{obj.name}' saved.")
        LogEntry.objects.log_action(
            user_id=request.user.pk,
            content_type_id=ContentType.objects.get_for_model(obj).pk,
            object_id=obj.pk,
            object_repr=force_str(obj),
            action_flag=CHANGE,
            change_message="Saved via admin panel",
        )

    def has_add_permission(self, request): return request.user.groups.filter(name="Drone Manager").exists() or request.user.is_superuser
    def has_change_permission(self, request, obj=None): return request.user.groups.filter(name="Drone Manager").exists() or request.user.is_superuser
    def has_delete_permission(self, request, obj=None): return request.user.is_superuser


# ------------------------- Matrix Admin -------------------------

@admin.register(Matrix)
class MatrixAdmin(admin.ModelAdmin):
    list_display = ("id", "max_x", "max_y", "visual_board")
    readonly_fields = ("id", "visual_board")
    search_fields = ("id",)
    inlines = [DroneInline]

    fieldsets = (
        (None, {"fields": ("id", "max_x", "max_y", "visual_board")}),
    )

    def visual_board(self, obj):
        drones = {(drone.x, drone.y): drone for drone in obj.drones.all()}

        orientation_icons = {
            "N": ("↑", "#2196F3"),
            "S": ("↓", "#E91E63"),
            "E": ("→", "#FF9800"),
            "O": ("←", "#4CAF50"),
        }

        cell_size = "45px" if max(obj.max_x, obj.max_y) <= 15 else "35px"
        rows = ""
        for y in range(obj.max_y):
            row = ""
            for x in range(obj.max_x):
                position = f"{x},{y}"
                drone = drones.get((x, y))

                if drone:
                    icon, color = orientation_icons.get(drone.orientation, ("?", "#000"))
                    drone_url = f"/admin/drones/drone/{drone.id}/change/"
                    content = (
                        f'<a href="{drone_url}" title="View Drone {drone.name}" style="text-decoration:none;">'
                        f'<div style="font-size:18px;color:{color};line-height:1;">{icon}</div>'
                        f'<div style="font-size:10px;color:black;">{position}</div>'
                        f'</a>'
                    )
                    style = (
                        f"background-color:#f0f0f0;text-align:center;font-weight:bold;"
                        f"border:1px solid #ccc;width:{cell_size};height:{cell_size};"
                        f"white-space:nowrap;overflow:hidden;"
                    )
                else:
                    content = f'<div style="font-size:10px;color:#999;">{position}</div>'
                    style = (
                        f"background:#fff;text-align:center;border:1px solid #eee;"
                        f"width:{cell_size};height:{cell_size};white-space:nowrap;overflow:hidden;"
                    )

                cell = f'<td style="{style}">{content}</td>'
                row += cell
            rows += f"<tr>{row}</tr>"

        table = (
            f'<div style="overflow:auto; max-width:100%;">'
            f'<table style="border-collapse:collapse;table-layout:fixed;">{rows}</table>'
            f'</div>'
        )
        return mark_safe(table)
    visual_board.short_description = "Drone Grid"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        LogEntry.objects.log_action(
            user_id=request.user.pk,
            content_type_id=ContentType.objects.get_for_model(obj).pk,
            object_id=obj.pk,
            object_repr=force_str(obj),
            action_flag=CHANGE,
            change_message="Saved via admin panel",
        )

    def has_add_permission(self, request): return request.user.groups.filter(name="Supervisor").exists() or request.user.is_superuser
    def has_change_permission(self, request, obj=None): return request.user.groups.filter(name="Supervisor").exists() or request.user.is_superuser
    def has_delete_permission(self, request, obj=None): return request.user.is_superuser


# ------------------------- Log Admin -------------------------

@admin.register(LogEntry)
class LogEntryAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ("action_time", "user", "content_type", "object_repr", "action_flag", "display_change_message", "colored_action")
    list_filter = ("user", "content_type", "action_flag")
    search_fields = ("object_repr", "change_message")

    def colored_action(self, obj):
        names = {1: "🟢 Created", 2: "🔵 Modified", 3: "🔴 Deleted"}
        colors = {1: "#4CAF50", 2: "#2196F3", 3: "#F44336"}
        return format_html('<span style="color:{}; font-weight:bold;">{}</span>', colors.get(obj.action_flag, "#000"), names.get(obj.action_flag, "❓"))
    colored_action.short_description = "Action"

    def display_change_message(self, obj):
        try:
            messages = json.loads(obj.change_message)
            return ", ".join(f"Changed: {', '.join(m['changed']['fields'])}" for m in messages if "changed" in m)
        except Exception:
            return obj.change_message
    display_change_message.short_description = "Details"

    def has_module_permission(self, request): return request.user.is_superuser
    def has_view_permission(self, request, obj=None): return request.user.is_superuser
