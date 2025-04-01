from django.contrib import admin, messages
from django import forms
from django.utils.safestring import mark_safe
from drones.infrastructure.models import Drone, Matrix


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

        if self.instance and hasattr(self.instance, "matrix") and self.instance.matrix:
            max_x = self.instance.matrix.max_x - 1
            max_y = self.instance.matrix.max_y - 1
        else:
            max_x = 100
            max_y = 100

        self.fields["x"].widget = forms.NumberInput(attrs={
            "min": 0,
            "max": max_x,
            "step": 1,
        })

        self.fields["y"].widget = forms.NumberInput(attrs={
            "min": 0,
            "max": max_y,
            "step": 1,
        })

    def clean(self):
        cleaned_data = super().clean()
        x = cleaned_data.get("x")
        y = cleaned_data.get("y")
        matrix = cleaned_data.get("matrix")

        if not matrix:
            self.add_error("matrix", "A matrix must be selected.")

        if x is not None and (x < 0 or x >= matrix.max_x):
            self.add_error("x", f"The X coordinate must be between 0 and {matrix.max_x - 1}")

        if y is not None and (y < 0 or y >= matrix.max_y):
            self.add_error("y", f"The Y coordinate must be between 0 and {matrix.max_y - 1}")

        if x is not None and y is not None and matrix:
            exists = Drone.objects.filter(
                matrix=matrix,
                x=x,
                y=y
            ).exclude(id=self.instance.id).exists()

            if exists:
                self.add_error(None, f"Another drone is already located at position ({x}, {y}) in this matrix.")

        return cleaned_data


class DroneInlineForm(forms.ModelForm):
    class Meta:
        model = Drone
        fields = ("name", "model", "x", "y", "orientation", "matrix")

    def clean(self):
        cleaned_data = super().clean()
        x = cleaned_data.get("x")
        y = cleaned_data.get("y")
        matrix = self.instance.matrix

        if x is not None and (x < 0 or x >= matrix.max_x):
            self.add_error("x", f"The X coordinate must be between 0 and {matrix.max_x - 1}")
        if y is not None and (y < 0 or y >= matrix.max_y):
            self.add_error("y", f"The Y coordinate must be between 0 and {matrix.max_y - 1}")

        if x is not None and y is not None:
            exists = Drone.objects.filter(
                matrix=matrix,
                x=x,
                y=y
            ).exclude(id=self.instance.id).exists()

            if exists:
                self.add_error(None, f"Another drone is already located at position ({x}, {y}) in this matrix.")

        return cleaned_data


class DroneInline(admin.TabularInline):
    model = Drone
    form = DroneInlineForm
    extra = 1
    fields = ("name", "model", "x", "y", "orientation")
    show_change_link = True


@admin.action(description="Reset position of selected drones")
def reset_position(modeladmin, request, queryset):
    queryset.update(x=0, y=0)
    messages.success(request, "Selected drones have been reset to position (0, 0).")


@admin.register(Drone)
class DroneAdmin(admin.ModelAdmin):
    form = DroneAdminForm
    list_display = ("id", "name", "model", "x", "y", "orientation", "matrix")
    list_editable = ("x", "y", "orientation", "matrix")
    search_fields = ("name", "model")
    list_filter = ("orientation", "matrix")
    readonly_fields = ("id",)
    autocomplete_fields = ("matrix",)
    actions = [reset_position]

    fieldsets = (
        ("Identification", {"fields": ("name", "model")}),
        ("Position", {
            "fields": ("x", "y", "orientation", "matrix"),
        }),
    )

    def save_model(self, request, obj, form, change):
        existing = Drone.objects.filter(
            matrix=obj.matrix,
            x=obj.x,
            y=obj.y
        ).exclude(id=obj.id)
        if existing.exists():
            messages.error(request, f"❌ Cannot save. Another drone already exists at position ({obj.x}, {obj.y}) in this matrix.")
            return 
        super().save_model(request, obj, form, change)
        messages.success(request, f"✅ Drone '{obj.name}' successfully saved.")


@admin.register(Matrix)
class MatrixAdmin(admin.ModelAdmin):
    list_display = ("id", "max_x", "max_y", "visual_board")
    readonly_fields = ("id", "visual_board")
    search_fields = ("id",)
    inlines = [DroneInline]

    def visual_board(self, obj):
        drones = {(drone.x, drone.y): drone for drone in obj.drones.all()}

        orientation_icons = {
            "N": ("↑", "#2196F3"),  # Azul
            "S": ("↓", "#E91E63"),  # Rosa
            "E": ("→", "#FF9800"),  # Naranja
            "O": ("←", "#4CAF50"),  # Verde
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
                    content = (
                        f'<div style="font-size:18px;color:{color};line-height:1;">{icon}</div>'
                        f'<div style="font-size:10px;">{position}</div>'
                    )
                    tooltip = f"Drone: {drone.name} | Model: {drone.model} | Orientation: {drone.orientation}"
                    style = (
                        f"background-color:#f0f0f0;text-align:center;font-weight:bold;"
                        f"border:1px solid #ccc;width:{cell_size};height:{cell_size};"
                        f"white-space:nowrap;overflow:hidden;"
                    )
                else:
                    content = f'<div style="font-size:10px;color:#999;">{position}</div>'
                    tooltip = ""
                    style = (
                        f"background:#fff;text-align:center;border:1px solid #eee;"
                        f"width:{cell_size};height:{cell_size};white-space:nowrap;overflow:hidden;"
                    )

                cell = f'<td title="{tooltip}" style="{style}">{content}</td>'
                row += cell
            rows += f"<tr>{row}</tr>"

        table = (
            f'<div style="overflow:auto; max-width:100%;">'
            f'<table style="border-collapse:collapse;table-layout:fixed;">{rows}</table>'
            f'</div>'
        )
        return mark_safe(table)
    visual_board.short_description = "Drone grid"

    fieldsets = (
        (None, {"fields": ("id", "max_x", "max_y", "visual_board")}),
    )
