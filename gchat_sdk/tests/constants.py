
SEND_MESSAGE_RESPONSE = {
    "status":"202",
    "msg":"Successfully added to the transmission queue","currentChatId":"6842ca3e7172a44adfadd510",
    "messageSentId":"6842cdafac5cfcd13012e45d"
}

CONTACT_DATA = {
    "id":"6569d66fa3544ba92d2f0cf3",
    "number":"5511997799298",
    "name":"Tatianno Alves"
}


CHAT_DATA_SEND_MESSAGE_EXCEPTION_CONTACT_TEST = {
    'chats': [
        {
            'attendanceId': '67feb3d68b3c33e700f09434', 
            'contact': {
                'id':'6569d66fa3544ba92d2f0cf3',
                'number':'5511997799298',
                'name':'Tatianno Alves'
            },
            'lastMessage': {
                'utcDhMessage': '2025-04-15T16:35:24.274', 
                'text': '🔼 Teste de mensagem', 
                'sender': {
                    'isMe': True
                }
            }
        }, 
        {
            'attendanceId': '67fea1efdd17283a1ac98fd1', 
            'contact': {
                'id': '663bc903df0d60792a7d1123', 
                'name': 'José', 
                'number': '551912341255'
            },
            'lastMessage': {
                'utcDhMessage': '2025-04-15T16:35:24.274',
                'text': '🔼 _*#Guilherme Carvalho:*_\nblz', 
                'sender': {
                   'isMe': True
                }
            }
        }
    ]
}


CHAT_DATA_SEND_MESSAGE_TEST = {
    'chats': [
        {
            'attendanceId': '67feb3d68b3c33e700f09434', 
            'contact': {
                'id': '6569d66fa3544ba92d2f0cf3', 
                'name': 'Tatianno', 
                'number': '5511997799298'
            },
            'lastMessage': {
                'utcDhMessage': '2025-04-15T19:35:49.005',
                'text': '🔼 _*#Thiago:*_\nBoa tarde Izabel voce poderia liberar o ndesk por favor?', 
                'sender': {
                    'isMe': True
                }
            }
        },
        {
            'attendanceId': '67fea1efdd17283a1ac98fd1', 
            'contact': {
                'id': '663bc903df0d60792a7d1122', 
                'name': 'Cleonice', 
                'number': '551912341234'
            },
            'lastMessage': {
                'utcDhMessage': '2025-04-15T19:49:24.274',
                'text': '🔼 _*#Guilherme Carvalho:*_\nblz', 
                'sender': {
                    'isMe': True
                }, 
            }
        }
    ]
}

CHAT_DATA_SEND_MESSAGE_WITH_ALERT_TEST = {
    'chats': [
        {
            'attendanceId': '67feb3d68b3c33e700f09434', 
            'contact': {
                'id': '6569d66fa3544ba92d2f0cf3', 
                'name': 'Tatianno', 
                'number': '5511997799298'
            }, 
            'lastMessage': {
                'text': '🔼 _*#Thiago:*_\nBoa tarde Izabel voce poderia liberar o ndesk por favor?', 
                'sender': {
                    'isMe': True
                }, 
                'utcDhMessage': '2025-04-15T19:49:49.005'
            }
        }, 
        {
            'attendanceId': '67fea1efdd17283a1ac98fd1', 
            'contact': {
                'id': '663bc903df0d60792a7d1122', 
                'name': 'Cleonice', 
                'number': '551912341234'
            },
            'lastMessage': {
                'utcDhMessage': '2025-04-15T19:35:24.274',
                'text': '🔼 _Você ainda está aí?', 
                'sender': {
                    'isMe': True
                }, 
            }
            
        }
    ]
}


CHAT_DATA = {
    'chats': [
        {
            'attendanceId': '67feb3d68b3c33e700f09434', 
            'contact': {
                'id': '6569d66fa3544ba92d2f0cf3', 
                'name': 'Tatianno',
                'number': '5511997799298'
            },
            'lastMessage': {
                'utcDhMessage': '2025-04-15T18:49:49.005',
                'text': '🔼 _*#Thiago:*_\nBoa tarde Izabel voce poderia liberar o ndesk por favor?', 
                'sender': {
                    'isMe': True
                }
            }
        },
        { 
            'attendanceId': '67fea1efdd17283a1ac98fd1', 
            'contact': {
                'id': '663bc903df0d60792a7d1122', 
                'name': 'Cleonice', 
                'number': '551912341234'
            },
            'lastMessage': {
                'utcDhMessage': '2025-04-15T16:56:24.274',
                'text': '🔼 _*#Guilherme Carvalho:*_\nblz', 
                'sender': {
                    'isMe': True
                },
            }
        },
        {
            'attendanceId': '67fea06c7d6367790067b4af', 
            'contact': {
                'id': '67e40c7f9738635732b524da', 
                'name': 'RAFAEL', 
                'number': '551121213322', 
            },
            'lastMessage': {
                'utcDhMessage': '2025-04-15T15:52:30', 
                'text': '🔽 Só me chamar aqui', 
                'sender': {
                    'isMe': False
                },
            }
        },
        { 
            'attendanceId': '67fe9d01d61e5036777e0ad6', 
            'contact': {
                'id': '67b63db6772c1c9244f1afe5', 
                'name': 'Stephanye',
                'number': '551744332233'
            },
            'lastMessage': {
                'utcDhMessage': '2025-04-15T18:00:33', 
                'text': '🔽 Oi pode ser amanhã \n\nMe desculpe não dará hoje', 
                'sender': {
                    'isMe': False
                }, 
            }
        }
    ]
}