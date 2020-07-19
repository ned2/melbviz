from functools import partial

from ipywidgets import (
    VBox,
    HBox,
    Dropdown,
    SelectMultiple,
    HTML,
    Output,
    interactive_output,
)


class PedestrianDemo:
    def prototype(self):
        """Create a prototype Dashboard"""
        # inputs
        year_input = Dropdown(options=self.years, description="Year")
        month_input = Dropdown(description="Month")
        sensor_input = SelectMultiple(description="Sensor", layout={"height": "150px"})
        def update_inputs(change):
            """Update available options for month and sensor inputs based on current year"""
            filtered_data = self.filter(year=year_input.value)
            # Need to temporarily disable all other custom handlers to prevent input
            # option changes triggering a UI update. (value changes are ok)
            month_handlers = month_input._trait_notifiers["value"]["change"]
            month_input._trait_notifiers["value"]["change"] = []
            month_input.options = filtered_data.months
            month_input._trait_notifiers["value"]["change"] = month_handlers
            month_input.value = None

            sensor_handlers = sensor_input._trait_notifiers["value"]["change"]
            sensor_input._trait_notifiers["value"]["change"] = []
            sensor_input.options = filtered_data.sensors
            sensor_input._trait_notifiers["value"]["change"] = sensor_handlers
            sensor_input.value = []
            
        year_input.observe(update_inputs, "value")
        year_input.value = self.years[-1]


        # outputs
        month_counts_output = interactive_output(
            self.make_callback("month_counts", height=350, width=550),
            {"sensor": sensor_input, "year": year_input},
        )
        sensor_counts_output = interactive_output(
            self.make_callback("sensor_counts", width=550),
            {"sensor": sensor_input, "year": year_input, "month": month_input},
        )
        sensors_map_output = interactive_output(
            self.make_callback("sensor_map", height=650, width=600),
            {"sensor": sensor_input, "year": year_input, "month": month_input},
        )
        sensors_traffic_output = interactive_output(
            self.make_callback("sensor_traffic", same_yscale=True, width=1200),
            {"sensor": sensor_input, "year": year_input, "month": month_input},
        )

        # layout
        title = HTML("<H1>Melbourne CBD Pedestrian Traffic</h1>")
        inputs = VBox([year_input, month_input, sensor_input])
        col1_row1 = HBox(
            [VBox([HBox([inputs]), month_counts_output]), sensors_map_output]
        )
        col1_row2 = sensors_traffic_output
        col1 = VBox([col1_row1, col1_row2])
        col2 = sensor_counts_output
        rows = [title, HBox([col1, col2])]
        return VBox(rows)
