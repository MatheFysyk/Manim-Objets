from manim import *

class Clock(VMobject):
    def __init__(
        self,
        radius: float = 0.7,
        clock_color: str = WHITE,
        stroke_width: float = 1.5,
        clock_hand_stroke_width: float = 3,
        tick_size_radius_ratio: float = 1 / 8,
        bigger_ticks_factor: float = 2,
        **kwargs
    ) -> None:
        self.radius = radius
        self.clock_color = clock_color
        self.stroke_width = stroke_width
        self.tick_size_radius_ratio = tick_size_radius_ratio
        self.bigger_ticks_factor = bigger_ticks_factor
        self.clock_hand_stroke_width = clock_hand_stroke_width
        self.clock_circle = Circle(radius, color=clock_color, stroke_width=stroke_width, **kwargs)

        super().__init__(**kwargs)        
        self.add(self.clock_circle)

        unit_tick = Line(ORIGIN, UP, color=clock_color, stroke_width=stroke_width, **kwargs)

        for k in range(12):
            tick = unit_tick.copy()
            if k % 3 == 0:
                tick.stretch_about_point(radius * tick_size_radius_ratio * bigger_ticks_factor, 1, unit_tick.get_start())
            else:
                tick.stretch_about_point(radius * tick_size_radius_ratio, 1, unit_tick.get_start())
            tick.rotate(k * (PI / 6), about_point=unit_tick.get_start())
            tick.shift((radius - tick.get_length()) * tick.get_unit_vector())
            self.add(tick)

        self.clock_hand = Line(ORIGIN, 0.8 * self[1].get_start(), stroke_width = clock_hand_stroke_width, **kwargs)
        self.add(self.clock_hand)

    def start(self, angular_velocity: float = 1):
        self.clock_hand.add_updater(lambda hand, dt: hand.rotate(-2 * PI * angular_velocity * dt, about_point=self.clock_circle.get_center()))
        return self

    def pause(self):
        self.clock_hand.remove_updater(*self.clock_hand.get_updaters())
        return self

    def get_time(self) -> float:
        return PI / 2 - self.clock_hand.get_angle()

    def time_to_angle(self, time: float = 0) -> float:
        return 2 * PI * time 

    def angle_to_time(self, angle: float = 0) -> float:
        return angle / (2 * PI)

    def set_time(self, time: float = 0):
        angle = self.get_time()
        new_angle = self.time_to_angle(time)
        self.clock_hand.rotate(angle - new_angle, about_point=self.clock_circle.get_center())
        return self

    def set_time_for_animations(self, time: float = 0) -> Rotate:
        return Rotate(self.clock_hand, self.get_time() - self.time_to_angle(time), about_point=self.clock_circle.get_center())


