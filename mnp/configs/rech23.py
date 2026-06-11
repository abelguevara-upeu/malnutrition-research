from typing import Dict, Any

config_f1: Dict[str, Any] = {
    'keys_to_cast': ['HHID'],
    'false_numerics': {
    "HV201": [
        10.0,
        20.0,
        40.0
    ],
    "HV204": [
        998.0
    ],
    "HV205": [
        10.0,
        20.0,
        30.0
    ],
    "HV237": [
        8.0
    ],
    "HV238": [
        98.0
    ],
    "SH58": [
        98.0
    ],
    "SH227": [
        9.0
    ],
    "QH227B": [
        7.0
    ],
    "HV213": [
        10.0,
        20.0,
        30.0
    ],
    "HV214": [
        10.0,
        20.0,
        30.0
    ],
    "HV215": [
        10.0,
        20.0,
        30.0
    ],
    "SH64": [
        96.0
    ],
    "SH66": [
        6.0
    ],
    "SH69": [
        8.0
    ],
    "SH76A": [
        8.0
    ],
    "SH78": [
        8.0
    ],
    "HV234": [
        994.0,
        995.0
    ],
    "HV220": [
        98.0
    ],
    "HV245": [
        96.0,
        98.0
    ],
    "HV246A": [
        98.0
    ],
    "HV246C": [
        98.0
    ],
    "HV246D": [
        98.0
    ],
    "HV246E": [
        98.0
    ],
    "HV246G": [
        98.0
    ],
    "HV246H": [
        98.0
    ],
    "HV246I": [
        98.0
    ],
    "HV246J": [
        98.0
    ]
},
    'divide_by_100000': ['HV271'],
    'cols_to_drop': [
    "HV202",
    "HV235",
    "HV237H",
    "HV237I",
    "HV237J",
    "HV237K",
    "HV237Z",
    "SH2212A",
    "SH2212B",
    "SH2212C",
    "SH2212D",
    "SH2212E",
    "SH2212F",
    "SH2213",
    "SH2407",
    "SH2408",
    "SH2409",
    "SH2410",
    "SH2605",
    "SH2606",
    "SH2607",
    "SH2802",
    "SH2803",
    "SH28EE",
    "HV227",
    "HV238",
    "HV239",
    "HV241",
    "HML1",
    "HML1A",
    "SH62",
    "SH72",
    "SH73",
    "SXH73",
    "SH108U",
    "SH108",
    "SH125U",
    "SH125",
    "SH225U",
    "SH225",
    "HV228",
    "HV248",
    "HV249",
    "HV250",
    "HV251",
    "HML2",
    "QH90",
    "QH90A",
    "QH91D",
    "QH91M",
    "QH91Y",
    "QH93",
    "QH94A",
    "QH94AB",
    "QH94B",
    "QH94BB",
    "QH94C",
    "QH94CB",
    "QH94D",
    "SHWLTHI2",
    "SHWLTHF2",
    "HV246B",
    "HV246F",
    "HV246K",
    "HV247",
    "SHVER",
    "SH31H",
    "SH31M",
    "SH81H",
    "SH81M",
    "SH90H",
    "SH90M",
    "SH82H",
    "SH82M",
    "SHEQUIPO",
    "SH01H",
    "SH01M"
],
    'coalesce': {
    "SH42_Agua_Todo_El_Dia": [
        "SH42_Agua_Todo_El_Dia",
        "SH2201",
        "SH32"
    ],
    "SH43": [
        "SH43",
        "SH2202",
        "SH33"
    ],
    "HV201": [
        "HV201",
        "SH2203"
    ],
    "SH48_Conserva_Agua": [
        "SH48_Conserva_Agua",
        "SH2204",
        "SH37"
    ],
    "SH51_Pago_Agua": [
        "SH51_Pago_Agua",
        "SH2208",
        "SH39"
    ],
    "SH52_Institucion_Agua": [
        "SH52_Institucion_Agua",
        "SH2209",
        "SH40"
    ],
    "SH51_Frec_Pago_Agua": [
        "SH51_Frec_Pago_Agua",
        "SH2210",
        "SH41"
    ],
    "HV205": [
        "HV205",
        "SH2401"
    ],
    "SH56_Frec_Limpieza": [
        "SH56_Frec_Limpieza",
        "SH2406",
        "SH46"
    ],
    "SH48_Basura": [
        "SH48_Basura",
        "SH2412"
    ],
    "SH58": [
        "SH58",
        "SH2412"
    ],
    "SH49_Frec_Basura": [
        "SH49_Frec_Basura",
        "SH2413"
    ],
    "SH59": [
        "SH59",
        "SH2413"
    ],
    "SH50_Tipo_Basurero": [
        "SH50_Tipo_Basurero",
        "SH2414"
    ],
    "SH60_Tipo_Basurero": [
        "SH60_Tipo_Basurero",
        "SH2414"
    ],
    "SH227": [
        "SH227",
        "SH110",
        "SH127"
    ],
    "SH61P": [
        "SH61P",
        "SH25F",
        "SH51P"
    ],
    "SH61Q": [
        "SH61Q",
        "SH25H",
        "SH51Q"
    ],
    "SH71": [
        "SH71",
        "SH26A",
        "SH61"
    ],
    "SH63": [
        "SH63",
        "SH2601",
        "SH53"
    ],
    "SH64": [
        "SH64",
        "SH2602",
        "SH54"
    ],
    "SH69": [
        "SH69",
        "SH2604"
    ],
    "SH60": [
        "SH60",
        "SH2609"
    ],
    "SH70_Fuente_Luz": [
        "SH70_Fuente_Luz",
        "SH2609"
    ],
    "SH67A": [
        "SH67A",
        "SH27CA"
    ],
    "SH77A": [
        "SH77A",
        "SH27CA"
    ],
    "SH76A": [
        "SH76A",
        "SH27CA",
        "SH67A",
        "SH77A"
    ],
    "SH67B": [
        "SH67B",
        "SH27CB"
    ],
    "SH77B": [
        "SH77B",
        "SH27CB"
    ],
    "SH76B": [
        "SH76B",
        "SH27CB",
        "SH67B",
        "SH77B"
    ],
    "SH67C": [
        "SH67C",
        "SH27CC"
    ],
    "SH77C": [
        "SH77C",
        "SH27CC"
    ],
    "SH76C": [
        "SH76C",
        "SH27CC",
        "SH67C",
        "SH77C"
    ],
    "SH67D": [
        "SH67D",
        "SH27CD"
    ],
    "SH77D": [
        "SH77D",
        "SH27CD"
    ],
    "SH76D": [
        "SH76D",
        "SH27CD",
        "SH67D",
        "SH77D"
    ],
    "SH67E": [
        "SH67E",
        "SH27CE"
    ],
    "SH77E": [
        "SH77E",
        "SH27CE"
    ],
    "SH76E": [
        "SH76E",
        "SH27CE",
        "SH67E",
        "SH77E"
    ],
    "SH78": [
        "SH78",
        "SH2801"
    ],
    "SH68F": [
        "SH68F",
        "SH28D"
    ],
    "SH78F": [
        "SH78F",
        "SH28D"
    ],
    "SH77F": [
        "SH77F",
        "SH28D",
        "SH68F",
        "SH78F"
    ],
    "SH61A": [
        "SH61A",
        "SH51A"
    ],
    "SH66": [
        "SH66",
        "HV240"
    ],
    "SH61B": [
        "SH61B",
        "SH51B"
    ],
    "SH61C": [
        "SH61C",
        "SH51C"
    ],
    "SH61D": [
        "SH61D",
        "SH51D"
    ],
    "SH61E": [
        "SH61E",
        "SH51E"
    ],
    "SH61J": [
        "SH61J",
        "SH51J"
    ],
    "SH61K": [
        "SH61K",
        "SH51K"
    ],
    "SH61L": [
        "SH61L",
        "SH51L"
    ],
    "SH61M": [
        "SH61M",
        "SH51M"
    ],
    "SH61N": [
        "SH61N",
        "SH51N"
    ],
    "SH61O": [
        "SH61O",
        "SH51O"
    ],
    "SH61R": [
        "SH61R",
        "SH51R"
    ],
    "SH61S": [
        "SH61S",
        "SH51S"
    ],
    "HV240": [
        "HV240",
        "SH66"
    ],
    "SH124": [
        "SH124",
        "SH107"
    ],
    "SH224": [
        "SH224",
        "SH107",
        "SH124"
    ],
    "HV234": [
        "HV234",
        "SH224"
    ],
    "HV270": [
        "HV270",
        "hv270"
    ],
    "HV271": [
        "HV271",
        "hv271"
    ],
    "SH52_Monto_Pago": [
        "SH52_Monto_Pago",
        "SH2211"
    ],
    "SH70_Hectareas": [
        "SH70_Hectareas",
        "SH28BB"
    ],
    "SH79": [
        "SH79",
        "SH28BB",
        "SH80"
    ]
},
}

config_f3 = {
    "HV201": 2018,
    "HV205": 2024,
    "HV225": 2024,
    "HV236": 2018,
    "HV237": 2024,
    "HV237A": 2024,
    "HV237B": 2024,
    "HV237C": 2024,
    "HV237D": 2024,
    "HV237E": 2024,
    "HV237F": 2024,
    "HV237G": 2024,
    "HV237X": 2024,
    "SH43": 2024,
    "SH58": 2018,
    "SH227": 2024,
    "QH227B": 2024,
    "HV207": 2024,
    "HV208": 2024,
    "HV209": 2024,
    "HV210": 2024,
    "HV211": 2024,
    "HV212": 2024,
    "HV213": 2024,
    "HV214": 2024,
    "HV215": 2024,
    "HV216": 2024,
    "HV221": 2024,
    "HV226": 2018,
    "HV242": 2024,
    "HV243A": 2024,
    "HV243B": 2024,
    "HV243C": 2024,
    "HV243D": 2024,
    "SH61A": 2024,
    "SH61B": 2024,
    "SH61C": 2024,
    "SH61D": 2024,
    "SH61E": 2024,
    "SH61J": 2024,
    "SH61K": 2024,
    "SH61L": 2024,
    "SH61M": 2024,
    "SH61N": 2024,
    "SH61O": 2024,
    "SH61P": 2024,
    "SH61Q": 2024,
    "SH61R": 2024,
    "SH61S": 2024,
    "SH63": 2024,
    "SH64": 2018,
    "SH66": 2024,
    "SH69": 2024,
    "SH71": 2024,
    "SH76A": 2024,
    "SH76B": 2024,
    "SH76C": 2024,
    "SH76D": 2024,
    "SH76E": 2024,
    "SH77F": 2024,
    "SH78": 2024,
    "HV206": 2024,
    "HV217": 2018,
    "HV219": 2024,
    "SHTOTH": 2024,
    "SH2211": 2007,
    "HV244": 2024,
    "HV246": 2024,
    # "HV270": 2024, # Ordinal puro (dejamos los números 1-5)
    # "HV271": 2024, # Continuo (factor de riqueza)
    "HV026": 2024,
    "HV040": 2024,
    "SHREGION": 2024,
    "SHPROVIN": 2024,
    "SHDISTRI": 2024,
    "UBIGEO": 2024,
    "ID1": 2024,
    "HHID": 2024,
    "HV218": 2024,
    "SHSEMES": 2024
}
