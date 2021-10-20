from loguru import logger
from db_query import *
from ask_permission_query import AMOZNO


# def defining_query(received_data: str) -> str:
#     inf_clint = received_data.split(" ")[0]
#     print(f"пришел запрос от клиента {inf_clint}")

#     if inf_clint == "ОТДОВАЙ":
#         return "GET"
#     elif inf_clint == "ЗОПИШИ":
#         return "PUT"
#     elif inf_clint == "УДОЛИ":
#         return "DELETE"
#     elif inf_clint == "GET" or "POST" or "PUT" or "DELETE":
#         return "HTTP(S)"
#     else:
#         print(f"Не разобрал тип запроса {inf_clint}")
#         return None





@logger.catch
def formation_response(received_data: str):
    inf_clint = received_data.split(" ")

    # inf_client_name = received_data.rpartition("РКСОК")[0][7:]
    # print(f"ПРЕОБРАЗОВАНИЕ {inf_client_name}")
    inf_client_name = received_data.split(" ")[1:-1]
    if len(inf_client_name) == 1:
        inf_client_name.append(" ")
        print("ЭТО ИМЯ КОТОРОЕ ПРИШЛО НА СЕРВЕР", inf_client_name)
        
    inf_client_phone = received_data.split("\r\n")[-3:-2]
    print("ЭТО НОМЕР КОТОРЫЙ ПРИШЕЛ НА СЕРВЕР", inf_client_phone)

    print(f"{inf_clint}\n{inf_client_name}\n{inf_client_phone}")

    if AMOZNO(inf_clint).split(" ")[0] == "МОЖНА":
        if inf_clint[0] == "ОТДОВАЙ":
            if inf_clint[0] == "ОТДОВАЙ" and check_record_db(" ".join(inf_client_name)) == True:                   
                return f"НОРМАЛДЫКС РКСОК/1.0\n{transaction_select(' '.join(inf_client_name))}\r\n\r\n"                  
            else:
                return "НИНАШОЛ РКСОК/1.0"


        elif inf_clint[0] == "ЗОПИШИ":
            if inf_clint[0] == "ЗОПИШИ" and check_record_db(" ".join(inf_client_name)) == True \
                or transaction_insert(" ".join(inf_client_name), inf_client_phone[0]) == False:
                return f"НИЛЬЗЯ РКСОК/1.0\nУже едем\r\n\r\n"
            else:
                transaction_insert(" ".join(inf_client_name), inf_client_phone[0])
                return "НОРМАЛДЫКС РКСОК/1.0"

        elif inf_clint[0] == "УДОЛИ":
            if inf_clint[0] == "УДОЛИ" and check_record_db(" ".join(inf_client_name)) == True:
                transaction_delete(" ".join(inf_client_name))
                return "НОРМАЛДЫКС РКСОК/1.0"
            else:
                return "НИНАШОЛ РКСОК/1.0"

        elif inf_clint[0] == "GET" or "POST" or "PUT" or "DELETE":
            return f"HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8\n\n" \
                    f"Привет! отживший своё протокол HTTP(S),<br /> Это Рабоче-Крестьянский Стандарт Отправки Команд 'РКСОК'"
        else:
            return "НИПОНЯЛ РКСОК/1.0"
    else:
        return f"НИЛЬЗЯ РКСОК/1.0\nЧто ещё за {' '.join(inf_client_name)} такой? Он тебе зачем?\r\n\r\n"


# @logger.catch
# async def formation_response(*received_data: str):
#     inf_clint = received_data.split(" ")

#     # inf_client_name = received_data.rpartition("РКСОК")[0][7:]
#     # print(f"ПРЕОБРАЗОВАНИЕ {inf_client_name}")
#     inf_client_name = received_data.split(" ")[1:-1]
#     if len(inf_client_name) == 1:
#         inf_client_name.append(" ")
#         print("ЭТО ИМЯ КОТОРОЕ ПРИШЛО НА СЕРВЕР", inf_client_name)
        
#     inf_client_phone = received_data.split("\r\n")[-3:-2]
#     print("ЭТО НОМЕР КОТОРЫЙ ПРИШЕЛ НА СЕРВЕР", inf_client_phone)

#     print(f"{inf_clint}\n{inf_client_name}\n{inf_client_phone}")

#     if await asyncio.run(AMOZNO(inf_clint).split(" ")[0]) == "МОЖНА":
#         if inf_clint[0] == "ОТДОВАЙ":
#             if inf_clint[0] == "ОТДОВАЙ" and check_record_db(" ".join(inf_client_name)) == True:                   
#                 return f"НОРМАЛДЫКС РКСОК/1.0\n{transaction_select(' '.join(inf_client_name))}\r\n\r\n"                  
#             else:
#                 return "НИНАШОЛ РКСОК/1.0"


#         elif inf_clint[0] == "ЗОПИШИ":
#             if inf_clint[0] == "ЗОПИШИ" and check_record_db(" ".join(inf_client_name)) == True \
#                 or transaction_insert(" ".join(inf_client_name), inf_client_phone[0]) == False:
#                 return f"НИЛЬЗЯ РКСОК/1.0\nУже едем\r\n\r\n"
#             else:
#                 transaction_insert(" ".join(inf_client_name), inf_client_phone[0])
#                 return "НОРМАЛДЫКС РКСОК/1.0"

#         elif inf_clint[0] == "УДОЛИ":
#             if inf_clint[0] == "УДОЛИ" and check_record_db(" ".join(inf_client_name)) == True:
#                 transaction_delete(" ".join(inf_client_name))
#                 return "НОРМАЛДЫКС РКСОК/1.0"
#             else:
#                 return "НИНАШОЛ РКСОК/1.0"

#         elif inf_clint[0] == "GET" or "POST" or "PUT" or "DELETE":
#             return f"HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8\n\n" \
#                     f"Привет! отживший своё протокол HTTP(S),<br /> Это Рабоче-Крестьянский Стандарт Отправки Команд 'РКСОК'"
#         else:
#             return "НИПОНЯЛ РКСОК/1.0"
#     else:
#         return f"НИЛЬЗЯ РКСОК/1.0\nЧто ещё за {' '.join(inf_client_name)} такой? Он тебе зачем?\r\n\r\n"
