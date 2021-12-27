from dataclasses import dataclass
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Возврщает сообщение о проведенных тренировках."""
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    H_IN_MIN: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            f'Не удалось получить калории в {self.__class__.__name__}')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        class_name: str = type(self).__name__
        return InfoMessage(class_name, self.duration, self.get_distance(),
                           self.get_mean_speed(), self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    K_RUN_1: int = 18
    K_RUN_2: int = 20

    def get_spent_calories(self) -> float:
        """Подсчет калорий."""
        calc_1: float = self.K_RUN_1 * self.get_mean_speed()
        calc_2: float = calc_1 - self.K_RUN_2
        calc_3: float = calc_2 * self.weight / self.M_IN_KM
        return calc_3 * (self.duration * self.H_IN_MIN)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба.
    height - рост."""

    K_WALK_1: float = 0.035
    K_WALK_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height: int = height

    def get_spent_calories(self) -> float:
        """Подсчет затраченных калорий."""
        calc_1: float = self.get_mean_speed() ** 2 // self.height
        calc_2: float = calc_1 * self.K_WALK_2 * self.weight
        calc_3: float = self.K_WALK_1 * self.weight + calc_2
        return calc_3 * (self.duration * self.H_IN_MIN)


class Swimming(Training):
    """Тренировка: плавание.
    length_pool - длина бассейна в метрах;
    count_pool - сколько раз пользователь переплыл бассейн."""

    LEN_STEP: float = 1.38
    K_SWIM_1: float = 1.1
    K_SWIM_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: int = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        """Переопределяет среднюю скорость движения."""
        calc: float = self.length_pool * self.count_pool / self.M_IN_KM
        return calc / self.duration

    def get_spent_calories(self) -> float:
        """Подсчет затраченных калорий."""
        calc: float = self.get_mean_speed() + self.K_SWIM_1
        return calc * self.K_SWIM_2 * self.weight


def read_package(training_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    code_training: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if training_type not in code_training:
        raise ValueError(
            f'Тип тренировки "{training_type}" '
            f'не найден в {type(code_training)}'
        )
    return code_training[training_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
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
