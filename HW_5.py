"""
1.	Доработать паука в имеющемся проекте, чтобы он складывал все записи в БД (любую)
и формировал item по структуре:
●	наименование вакансии;
●	зарплата от;
●	зарплата до;
●	ссылка на саму вакансию;
●	сайт, откуда собрана вакансия.
2.	Создать в имеющемся проекте второго паука по сбору вакансий с сайта superjob. Паук должен формировать
item по аналогичной структуре и складывать данные в БД.
3.	Взять любую категорию товаров на сайте Леруа Мерлен. Собрать с использованием ItemLoader следующие данные:
●	название;
●	все фото;
●	параметры товара в объявлении.
4.	С использованием output_processor и input_processor реализовать очистку и преобразование данных.
Цены должны быть в виде числового значения.
5.	*Написать универсальный обработчик параметров объявлений, который будет формировать данные
вне зависимости от их типа и количества.
6.	*Реализовать более удобную структуру для хранения скачиваемых фотографий.
Дополнительно:
Перевести всех пауков сбора данных о вакансиях на ItemLoader и привести к единой структуре.
Сайт можно взять и любой друго й (интернет-магазин или сайт с объявлениями отсюда). Главное, чтобы
по get-запросу вам возвращалась нужная информация.
"""