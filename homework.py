class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = round(duration, 3)
        self.distance = round(distance, 3)
        self.speed = round(speed, 3)
        self.calories = round(calories, 3)

    def get_message(self):
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


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
        self.workout_type = ''

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * Training.LEN_STEP / Training.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.workout_type,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIE_1 = 18
    COEFF_CALORIE_2 = 20
    COEFF_CALORIE_3 = 60

    def __init__(self, action, duration, weight):

        super().__init__(action, duration, weight)
        self.workout_type = self.__class__.__name__

    def get_spent_calories(self):

        coef_return_1 = Running.COEFF_CALORIE_1 * super().get_mean_speed()
        coef_return_3 = self.duration * Running.COEFF_CALORIE_3
        coef_return_4 = coef_return_1 - Running.COEFF_CALORIE_2

        return (coef_return_4) * self.weight / Training.M_IN_KM * (coef_return_3)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CALORIE_1 = 0.035
    COEFF_CALORIE_2 = 2
    COEFF_CALORIE_3 = 0.029
    COEFF_CALORIE_4 = 60

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height
        self.workout_type = self.__class__.__name__

    def get_spent_calories(self):

        coef_return_1 = SportsWalking.COEFF_CALORIE_1 * self.weight
        coef_return_2 = super().get_mean_speed() ** SportsWalking.COEFF_CALORIE_2
        coef_return_3 = SportsWalking.COEFF_CALORIE_3 * self.weight
        coef_return_4 = self.duration * SportsWalking.COEFF_CALORIE_4
        coef_return_5 = coef_return_2 // self.height

        return (coef_return_1 + coef_return_5 * coef_return_3) * coef_return_4


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    COEFF_CALORIE_1 = 1.1
    COEFF_CALORIE_2 = 2

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.workout_type = self.__class__.__name__
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self):

        return self.action * Swimming.LEN_STEP / Training.M_IN_KM

    def get_mean_speed(self):

        return self.length_pool * self.count_pool / Training.M_IN_KM / self.duration

    def get_spent_calories(self):

        coef_return_1 = self.get_mean_speed() + Swimming.COEFF_CALORIE_1
        coef_return_2 = Swimming.COEFF_CALORIE_2 * self.weight

        return coef_return_1 * coef_return_2


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    work_types = {
        'RUN': Running,
        'SWM': Swimming,
        'WLK': SportsWalking
    }

    if workout_type not in work_types:
        return print('Ошибка!')

    work_type_class = work_types[workout_type]
    return work_type_class(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
