class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = round(duration, 3)
        self.distance = round(distance, 3)
        self.speed = round(speed, 3)
        self.calories = round(calories, 3)

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; Длительность: {self.duration:.3f} ч.; Дистанция: {self.distance:.3f} км; Ср. скорость: {self.speed:.3f} км/ч; Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self, workout_type, duration, distance, speed, calories) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(workout_type, duration, distance, speed, calories)
        return info.get_message()


class Running(Training):
    """Тренировка: бег."""

    def __init__(self, action, duration, weight):

        super().__init__(action, duration, weight)
        self.M_IN_KM = 1000
        self.workout_type = 'Running'

    def get_spent_calories(self):

        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        coeff_calorie_3 = 60

        return (coeff_calorie_1 * super().get_mean_speed() - coeff_calorie_2) * self.weight / self.M_IN_KM * (self.duration * coeff_calorie_3)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height
        self.workout_type = 'SportsWalking'

    def get_spent_calories(self):

        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 2
        coeff_calorie_3 = 0.029
        coeff_calorie_4 = 60

        return (coeff_calorie_1 * self.weight + (super().get_mean_speed() ** coeff_calorie_2 // self.height) * coeff_calorie_3 * self.weight) * (self.duration * coeff_calorie_4)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.M_IN_KM = 1000
        self.workout_type = 'Swimming'
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):

        return self.length_pool * self.count_pool / self.M_IN_KM / self.duration

    def get_spent_calories(self):

        coeff_calorie_1 = 1.1
        coeff_calorie_2 = 2

        return (self.get_mean_speed() + coeff_calorie_1) * coeff_calorie_2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type == 'RUN':
        return Running(data[0], data[1], data[2])

    elif workout_type == 'SWM':
        return Swimming(data[0], data[1], data[2], data[3], data[4])

    else:
        return SportsWalking(data[0], data[1], data[2], data[3])


def main(training: Training) -> None:
    """Главная функция."""
    message = training.show_training_info(training.workout_type, training.duration, training.get_distance(), training.get_mean_speed(), training.get_spent_calories())
    print(message)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
