from manim import *

g = 1

class Pendulum(VMobject):
    def __init__(
        self,
        rod_length: float = 3,
        angle_value: float = PI / 6,
        rod_color: float = YELLOW,
        mass_value: float = 1,
        mass_radius: float = 0.2,
        mass_color: str = WHITE,
        add_angle_label: bool = True,
        **kwargs 
    ) -> None:
        self.rod_length = rod_length
        self.rod_color = rod_color
        self.mass_value = mass_value
        self.mass_radius = mass_radius
        self.mass_color = mass_color
        super().__init__(**kwargs)

        self.pendulum_state = np.array([angle_value, 0])

        self.rod = Line(ORIGIN, rod_length * RIGHT, color=rod_color, **kwargs).rotate(angle_value - PI / 2, about_point=ORIGIN)
        self.mass = Circle(mass_radius, color=mass_color, fill_opacity=1, **kwargs).move_to(self.rod.get_end())
        self.dashed_vertical_line = DashedLine(ORIGIN, rod_length / 1.5 * DOWN)
        self.add(self.rod, self.mass, self.dashed_vertical_line)

        if add_angle_label:
            try:
                self.angle = Angle(self.rod, self.dashed_vertical_line, rod_length / 5, other_angle=(angle_value > 0))
                self.angle_label = MathTex(
                    r"\theta"
                ).move_to(Angle(self.rod, self.dashed_vertical_line, radius=1.6 * self.angle.radius, other_angle=(angle_value > 0)).point_from_proportion(0.5))
                self.rod.set_z_index(self.angle.z_index + 1)
                self.dashed_vertical_line.set_z_index(self.angle.z_index + 1)
                self.mass.set_z_index(self.rod.z_index + 1)
                self.add(self.angle, self.angle_label)
            except ValueError:
                self.angle_label = MathTex(r"\theta").move_to(self.rod.get_start() + 1.6 * rod_length / 5 * self.rod.get_unit_vector())
    
    def get_pendulum_angle(self) -> float:
        return self.pendulum_state[0]

    def get_pendulum_angular_velocity(self) -> float:
        return self.pendulum_state[1]

    def set_pendulum_state(self, angle: float, angular_velocity: float):
        self.pendulum_state[0] = angle
        self.pendulum_state[1] = angular_velocity
        return self

    def start_bouncing(self, init_velocity: float = 0):
        self.set_pendulum_state(self.get_pendulum_angle(), init_velocity)

        def pendulum_eq(Y):
            theta, dtheta = Y
            return np.array([dtheta, -g / self.rod_length * np.sin(theta)])
        
        def pendulum_updater(pendulum, dt):
            k_1 = pendulum_eq(pendulum.pendulum_state)
            k_2 = pendulum_eq(pendulum.pendulum_state + dt / 2 * k_1)
            k_3 = pendulum_eq(pendulum.pendulum_state + dt / 2 * k_2)
            k_4 = pendulum_eq(pendulum.pendulum_state + dt * k_3)
            dY = dt / 6 * (k_1 + 2 * k_2 + 2 * k_3 + k_4)
            pendulum.pendulum_state += dY
            pendulum.rod.rotate(dY[0], about_point=pendulum.rod.get_start())
            pendulum.mass.move_to(pendulum.rod.get_end())
            pendulum.angle.become(Angle(pendulum.rod, self.dashed_vertical_line, pendulum.rod_length / 5, other_angle=(pendulum.pendulum_state[0] > 0)))
            try:
                self.angle_label.move_to(
                    Angle(pendulum.rod, pendulum.dashed_vertical_line, radius=1.6 * self.angle.radius, other_angle=(pendulum.pendulum_state[0] > 0)
                ).point_from_proportion(0.5))
            except ValueError:
                self.angle_label.move_to(pendulum.rod.get_start() + 1.6 * pendulum.rod_length / 5 * pendulum.rod.get_unit_vector())
        
        self.add_updater(pendulum_updater)
        return self

    def stop_bouncing(self):
        self.remove_updater(*self.get_updaters())
        return self
