from pathlib import Path


"""
------------------------------------------------GENERAL SETTINGS--------------------------------------------------------
    WALLETS_TO_WORK = 0 | Софт будет брать кошельки из таблице по правилам, описанным снизу
    0       = все кошельки подряд
    3       = только кошелек №3
    4, 20   = кошелек №4 и №20
    [[5, 25]] = кошельки с №5 по №25
    [[5, 25], [30, 35]] = кошельки с №5 по №25 и с №30 по №30

    WALLETS_TO_EXCLUDE = 0 | Софт будет исключать кошельки из таблицы по правилам, описанным снизу
    0       = никакой кошелек не будет убран
    3       = только кошелек №3
    4, 20   = кошелек №4 и №20
    [5, 25] = кошельки с №5 по №25
    [[5, 25], [30, 35]] = кошельки с №5 по №25 и с №30 по №30

    ACCOUNTS_IN_STREAM      | Количество кошельков в потоке на выполнение. Если всего 100 кошельков, а указать 10,
                                то софт сделает 10 подходов по 10 кошельков
    CONTROL_TIMES_FOR_SLEEP | Количество проверок, после которого для всех аккаунтов будет включен рандомный сон в
                                моменте, когда газ опуститься до MAXIMUM_GWEI и аккаунты продолжат работать

    EXCEL_PASSWORD          | Включает запрос пароля при входе в софт. Сначала установите пароль в таблице
    EXCEL_PAGE_NAME         | Название листа в таблице. Пример: 'EVM'
    GOOGLE_SHEET_URL        | Ссылка на вашу Google таблицу с прогрессом аккаунтов
    GOOGLE_SHEET_PAGE_NAME  | Аналогично EXCEL_PAGE_NAME
    MAIN_PROXY              | Прокси для обращения к API бирж. Формат - log:pass@ip:port. По умолчанию - localhost
"""
SOFTWARE_MODE = 0               # 0 - последовательный запуск / 1 - параллельный запуск
ACCOUNTS_IN_STREAM = 1          # Только для SOFTWARE_MODE = 1 (параллельный запуск)
WALLETS_TO_WORK = 0             # 0 / 3 / 3, 20 / [3, 20] / [[1, 10], [20, 25]]
WALLETS_TO_EXCLUDE = 0          # 0 / 3 / 3, 20 / [3, 20] / [[1, 10], [20, 25]]
SHUFFLE_WALLETS = True         # Перемешивает кошельки перед запуском
SHUFFLE_ROUTE = False           # Перемешивает маршрут перед запуском
BREAK_ROUTE = False             # Прекращает выполнение маршрута, если произойдет ошибка
STOP_SOFTWARE = False           # Прекращает выполнение всего софта, если произойдет критическая ошибка
SAVE_PROGRESS = True            # Включает сохранение прогресса аккаунта для Classic-routes
TELEGRAM_NOTIFICATIONS = False  # Включает уведомления в Telegram

'------------------------------------------------SLEEP CONTROL---------------------------------------------------------'
SLEEP_MODE = True                # Включает сон после каждого модуля и аккаунта
SLEEP_TIME_MODULES = (20, 30)  # (минимум, максимум) секунд | Время сна между модулями.
SLEEP_TIME_ACCOUNTS = (40, 60)   # (минимум, максимум) секунд | Время сна между аккаунтами.

'-----------------------------------------------------GAS CONTROL------------------------------------------------------'
GAS_CONTROL = False             # Включает контроль газа
MAXIMUM_GWEI = 40               # Максимальный GWEI для работы софта, изменять во время работы софта в maximum_gwei.json
SLEEP_TIME_GAS = 100            # Время очередной проверки газа
CONTROL_TIMES_FOR_SLEEP = 5     # Количество проверок
GAS_LIMIT_MULTIPLIER = 1.5      # Множитель газ лимита для транзакций. Поможет сэкономить на транзакциях
GAS_PRICE_MULTIPLIER = 1.5      # Множитель цены газа для транзакций. Ускоряет выполнение или уменьшает цену транзакции

'-----------------------------------------------------RETRY CONTROL----------------------------------------------------'
MAXIMUM_RETRY = 20              # Количество повторений при ошибках
SLEEP_TIME_RETRY = (5, 10)      # (минимум, максимум) секунд | Время сна после очередного повторения

'-----------------------------------------------SLIPPAGE CONTROL-------------------------------------------------------'
SLIPPAGE = 3                  # 0.54321 = 0.54321%, 1 = 1% | Максимальное влияние на цену при обменах токенов

'----------------------------------------------------APPROVE CONTROL---------------------------------------------------'
UNLIMITED_APPROVE = True       # Включает безлимитный Approve для контракта

'------------------------------------------------------REF SISTEM------------------------------------------------------'
REF_LINK_DEBRDIGE = [18984]   # Укажите здесь свою реферальную ссылку и все аккаунты будут делать бриджи по ней

'-----------------------------------------------------HELP SOFTWARE----------------------------------------------------'
HELP_SOFTWARE = False   # Если True, с минтов на GetMint и Womex автору будет уходить копейка, цена на минт не меняется

'-----------------------------------------------------PROXY CONTROL----------------------------------------------------'
USE_PROXY = False                # Включает использование прокси
MOBILE_PROXY = False             # Включает использование мобильных прокси. USE_PROXY должен быть True
MOBILE_PROXY_URL_CHANGER = [
    '',
]  # ['link1', 'link2'..] | Ссылки для смены IP. Софт пройдется по всем ссылкам

MAIN_PROXY = ''                  # log:pass@ip:port, прокси для обращения к API бирж. По умолчанию - localhost

'-----------------------------------------------------SECURE DATA------------------------------------------------------'
# OKX API KEYS https://www.okx.com/ru/account/my-api
OKX_API_KEY = ""
OKX_API_SECRET = ""
OKX_API_PASSPHRAS = ""
OKX_EU_TYPE = False

# BITGET API KEYS https://www.bitget.com/ru/account/newapi
BITGET_API_KEY = ""
BITGET_API_SECRET = ""
BITGET_API_PASSPHRAS = ""

# BINGX API KEYS https://bingx.com/ru-ru/account/api/
BINGX_API_KEY = ""
BINGX_API_SECRET = ""

# BINANCE API KEYS https://www.binance.com/ru/my/settings/api-management
BINANCE_API_KEY = ""
BINANCE_API_SECRET = ""

current_dir = Path(__file__).parent
EXCEL_FILE_PATH = current_dir / 'data' / 'accounts_data.xlsx'

# EXCEL AND GOOGLE INFO
EXCEL_PASSWORD = False
EXCEL_PAGE_NAME = "EVM"
# Можете не изменять, если устраивает дефолтное расположение таблицы
GOOGLE_SHEET_URL = ""
GOOGLE_SHEET_PAGE_NAME = ""

# TELEGRAM DATA
TG_TOKEN = "7477351518:AAGoAK7o41xH1PnbVoWAAsQ5DM4tvIrkXzU"  # https://t.me/BotFather
TG_ID = "7477351518"  # https://t.me/getmyid_bot

# INCH API KEY https://portal.1inch.dev/dashboard
ONEINCH_API_KEY = ""

# LAYERSWAP API KEY https://www.layerswap.io/dashboard
LAYERSWAP_API_KEY = ""

'-----------------------------------------------------SAVE LOGS TO DB--------------------------------------------------'

SAVE_LOGS_TO_DATABASE = False             # Опция записи логов базу данных MSSQL (по умолчанию отключена)
DB_HOST = ''                              # Хост сервера
DB_NAME = ''                              # Имя базы данных
DB_USERNAME = ''                          # Имя пользователя
DB_PASSWORD = ''                          # Пароль
