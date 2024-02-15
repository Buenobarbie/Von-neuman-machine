class C3PO:
	def __init__(self, language):
		if language not in ["en","pt","es","tl"]: raise ValueError("Language not suported")
		self.language=language
		self.message={
			"languages":{
				"en":"English",
				"pt":"Portugûes",
				"es":"Español",
				"tl":"TlhIngan Hol"
			},
			"help":{
				"en":" COMMAND  PARAMETERS           OPERATION\n---------------------------------------------------------------------------\n    i                          Restart MVN\n    p     [file]               Load program to memory\n    r     [addr] [regs]        Run program\n    b                          Activate/Deactivate debug mode\n    s                          Manage I/O devices\n    g                          List register content\n    m     [ini] [end]          List memory content\n    h                          Help \n    x                          End MVN and terminal",
				"pt":" COMANDO  PARÂMETROS           OPERAÇÃO\n---------------------------------------------------------------------------\n    i                          Reinicia MVN\n    p     [arq]                Carrega programa para a memória\n    r     [ende] [regs]        Executa o programa\n    b                          Ativa/Desativa modo Debug\n    s                          Manipula dispositivos de I/O\n    g                          Lista conteúdo dos registradores\n    m     [ini] [fim]          Lista conteúdo da memória\n    h                          Ajuda\n    x                          Finaliza MVN e terminal",
				"es":" COMANDO  PARÁMETROS           OPERACIÓN\n---------------------------------------------------------------------------\n    i                          Reinicia MVN\n    p     [arq]                Carga el programa a la memoria\n    r     [posi] [regs]        Executa el programa\n    b                          Activa/Desactiva el modo Debug\n    s                          Manipula los dispositivos de I/O\n    g                          Lista contenido de los registros\n    m     [ini] [fim]          Lista contenido de la memoria\n    h                          Ayuda\n    x                          Cerra MVN e terminal",
				"tl":"   ra'    De'Wa'DIch           QapwI'\n---------------------------------------------------------------------------\n    i                          MVN taghqa'lu'\n    p     [navDe'wI']          qawHaqvaD ghun qenglu'\n    r     [Daq] [De'jan]       ghun De'wI'Qaplu'\n    b                          chu'lu'/chu'be'lu' Debug Qap\n    s                          jan I/O vu'lu'\n    g                          De'jan 'anglu'\n    m     [wa'DIch] [Qav]      qawHaq 'anglu'\n    h                          QaH\n    x                          MVN jIH je rInlu'"
			},
			"dbg_help":{
				"en":" COMMAND  PARAMETERS           OPERATION\n---------------------------------------------------------------------------\n    c                          Continue execution\n    s                          Make one step forward on execution\n    b     [addr]               Insert a breakpoint\n    x                          Pause execution\n    h                          Help\n    r     [reg] [val]          Place value on register\n    a     [addr] [val]         Place value in memory\n    e                          Show register values\n    m     [ini] [fim]          List memory content",
				"pt":" COMANDO  PARÂMETROS           OPERAÇÃO\n---------------------------------------------------------------------------\n    c                          Continua execução\n    s                          Avança um passo na execução\n    b     [ende]               Insere um breakpoint\n    x                          Pausa execução\n    h                          Ajuda\n    r     [reg] [val]          Atribui valor a registrador\n    a     [ende] [val]         Atribui valor a memória\n    e                          Mostra valores dos registradores\n    m     [ini] [fim]          Lista conteúdo da memória",
				"es":" COMANDO  PARÁMETROS           OPERACIÓN\n---------------------------------------------------------------------------\n    c                          Continua execución\n    s                          Avanza um passo en la execución\n    b     [posi]               Insere un breakpoint\n    x                          Pausa execusión\n    h                          Ayuda\n    r     [reg] [val]          Atribuye valor a un registro\n    a     [posi] [val]         Atribuye valor a memoria\n    e                          Muestra valores de los registradores\n    m     [ini] [fim]          Lista contenido de la memória",
				"tl":"   ra'    De'Wa'DIch           QapwI'\n---------------------------------------------------------------------------\n    c                          De'wI'Qapqa'lu'\n    s                          wa' gho' De'wI'Qaplu' \n    b     [Daq]                Breakpoint chellu'\n    x                          De'wI'Qap rInlu'\n    h                          QaH\n    r     [De'qawHaq] [mI']    De'qawHaqvaD  mI' chellu'\n    a     [Daq] [mI']          qawHaqvaD mI' chellu'\n    e                          De'qawHaq 'anglu'\n    m     [wa'DIch] [Qav]      qawHaq 'anglu'"
			},
			"header":{
				"en":"                Escola Politécnica da Universidade de São Paulo\n                   PCS3616 - von Neumann Machine Simulator\n                 MVN version %s (%s) - All rights reserved",
				"pt":"                Escola Politécnica da Universidade de São Paulo\n                 PCS3616 - Simulador da Máquina de von Neumann\n              MVN versão %s (%s) - Todos os direitos reservados",
				"es":"                Escola Politécnica da Universidade de São Paulo\n               PCS3616 - Simulador de  la Máquina de von Neumann\n             MVN versión %s (%s) - Todos os derechos reservados",
				"tl":"                Escola Politécnica da Universidade de São Paulo\n                       PCS3616 - von Neumann jo' ngebwI'\n                    MVN DaHQap %s (%s) - lugh Hoch choqta'"
			},
			"MVN_ini":{
				"en":"MVN started",
				"pt":"MVN iniciada",
				"es":"MVN iniciada",
				"tl":"MVN taghlu'ta'"
			},
			"disp_ini_arq":{
				"en":"Devices from 'disp.lst' started",
				"pt":"Dispositivos de 'disp.lst' iniciados",
				"es":"Dispositivos de 'disp.lst' iniciados",
				"tl":"'disp.lst' jan taghlu'ta'"
			},
			"disp_ini_def":{
				"en":"Default devices start",
				"pt":"Inicializacao padrão de dispositivos",
				"es":"Bota estándar de dispositivos",
				"tl":"jan motlh tagh"
			},
			"dev_head":{
				"en":"Type   CU   Device\n----------------------------------",
				"pt":"Tipo   UC   Dispositivo\n----------------------------------",
				"es":"Tipo   UC   Dispositivo\n----------------------------------",
				"tl":"Segh   Sj   jan\n----------------------------------"
			},
			"reg_head":{
				"en":" MAR  MDR  IC   IR   OP   OI   AC\n---- ---- ---- ---- ---- ---- ----",
				"pt":" MAR  MDR  IC   IR   OP   OI   AC\n---- ---- ---- ---- ---- ---- ----",
				"es":" MAR  MDR  IC   IR   OP   OI   AC\n---- ---- ---- ---- ---- ---- ----",
				"tl":" MAR  MDR  IC   IR   OP   OI   AC\n---- ---- ---- ---- ---- ---- ----"
			},
			"big_instru":{
				"en":"More than two numbers on the instruction",
				"pt":"Mais de dois números na instrução",
				"es":"Más de dos numeros en la instrucción",
				"tl":"cha' mI' law' ra' mI' puS"
			},
			"big_number":{
				"en":"Number is too big for the MVN",
				"pt":"Número é grande demais para a MVN",
				"es":"Número és demasiado grande para la MVN",
				"tl":"MVNvaD tlhoy tIn mI'"
			},
			"loaded":{
				"en":"Program %s loaded",
				"pt":"Programa %s carregado",
				"es":"Programa %s cargado",
				"tl":"ghun %s qenglu'ta'"
			},
			"yes":{
				"en":"y",
				"pt":"s",
				"es":"s",
				"tl":"H"
			},
			"no":{
				"en":"n",
				"pt":"n",
				"es":"n",
				"tl":"g"
			},
			"show_regs":{
				"en":"Show registers values at each step of the FDE cycle? <y/n> [%s]: ",
				"pt":"Exhibir valores de los registros a cada passo do ciclo FDE? <s/n> [%s]: ",
				"es":"Exibir valores dos registradores en cada passo del ciclo FDE? <s/n> [%s]: ",
				"tl":"De'qawHaq 'ang'a' gho'qa' bav FDE? <H/g> [%s]: "
			},
			"step_by_step":{
				"en":"Execute MVN step by step? <y/n> [%s]: ",
				"pt":"Executar a MVN passo a passo? <s/n> [%s]: ",
				"es":"Ejecutar la MVN paso a paso? <s/n> [%s]: ",
				"tl":"MVN De'wI'Qap'a' gho'qa? <H/g> [%s]: "
			},
			"infty_loop":{
				"en":"Steps limit hit, check if there are infinite loops",
				"pt":"Limite de passos atingido, verifique se não há loops infinitos",
				"es":"Límite de pasos alcanzado, checa si no hay ciclos infinitos",
				"tl":"gho' veH SIchta', bav vuSbe' yI''ol"
			},
			"start":{
				"en":"Starting simulation",
				"pt":"Começando simulação",
				"es":"Comezando simulación",
				"tl":"ngeb taghlI'"
			},
			"dbg_comm":{
				"en":"dbg commands are",
				"pt":"Os comandos do dbg são",
				"es":"Los comandos de dbg son",
				"tl":"ra' dbg chaH"
			},
			"break_hex":{
				"en":"Breakpoint has to be hexadecimal values",
				"pt":"Breakpoint deve ser um valor inteiro hexadecimal",
				"es":"Breakpoint tiene que ser un valor hexadecimal",
				"tl":"wa'maH jav pat HnIS breakpoint"
			},
			"no_addr":{
				"en":"No address was given in the instruction",
				"pt":"Nenhum endereço passado na instrução",
				"es":"Ninguna posición passada en la instrucción",
				"tl":"ra' nob Daq pagh"
			},
			"reg_inv":{
				"en":"Invalid register",
				"pt":"Registrador invalido",
				"es":"Registro invalido",
				"tl":"De'qawHaq Hatcd"
			},
			"val_hex":{
				"en":"Memory addresses and values must be hexadecimal",
				"pt":"Enderecos de memória e valores devem ser hexadecimais",
				"es":"Posiciónes de memoria y valores tienen que ser hexadecimais",
				"tl":"wa'maH jav HnIS qawHaq Daq mI' je"
			},
			"no_rec":{
				"en":"Command not recognized\nPress h for help",
				"pt":"Comando não reconhecido\nPressione h para ajuda",
				"es":"Comando no reconocido\nPulsa h para ayuda",
				"tl":"ghovbe'lu' ra'\nh yI'uymeH QaH"
			},
			"int_val":{
				"en":"%s value must be integer, using default value",
				"pt":"O valor de %s deve ser inteiro, usando valor padrão.",
				"es":"El valor de %s tiene que ser entero, utilizando el valor estándar",
				"tl":"naQ HnIS %s mI', mI' motlh lo'taH"
			},
			"inp_file":{
				"en":"Inform input file name: ",
				"pt":"Informe o nome do arquivo de entrada: ",
				"es":"Informa el nombre del archivo de entrada: ",
				"tl":"pongDaj navDe'wIDaj 'el yI'nob: "
			},
			"big_file":{
				"en":"File must be 1 word long, %s given",
				"pt":"Arquivo deve ter 1 palavra, %s passadas",
				"es":"Archivo tiene que ter 1 palabra, %s dadas",
				"tl":"wa' pong yI'ngaS ngaS navDe'wI, nobta' %s"
			},
			"inf_IC":{
				"en":"Inform IC address [%s]: ",
				"pt":"Informe o endereco do IC [%s]: ",
				"es":"Informa la posición del IC [%s]: ",
				"tl":"qawHaqDaqDaj IC yI'nob [%s]: "
			},
			"cant_run":{
				"en":"No file was loaded, nothing to be executed",
				"pt":"Nenhum arquivo foi carregado, nada a ser executado",
				"es":"Ningún archivo fue cargado, nada a ser ejecutado",
				"tl":"qengta' pagh navDe'wI, De'wI'Qaplu' pagh"
			},
			"deb_on":{
				"en":"Debugger mode activated",
				"pt":"Modo debugger ativado",
				"es":"modo debugger activado",
				"tl":"chu'ta' debugger Qap"
			},
			"deb_off":{
				"en":"Debugger mode deactivated",
				"pt":"Modo debugger desativado",
				"es":"modo debugger desactivado",
				"tl":"chu'be'ta' debugger Qap"
			},
			"dev_deal":{
				"en":"Add (a) or remove (r) (ENTER to cancel): ",
				"pt":"Adicionar (a) ou remover (r) (ENTER para cancelar): ",
				"es":"Adicionar (a) o remover (r) (ENTER para cancelar): ",
				"tl":"chel (a) qoj teq (r) (ENTER qIlmeH): "
			},
			"dev_type":{
				"en":"Device type (ENTER to cancel): ",
				"pt":"Tipo de dispositivo (ENTER para cancelar): ",
				"es":"Tipo de dispositivo (ENTER para cancelar): ",
				"tl":"SeghDaj jan (ENTER qIlmeH): "
			},
			"dev_UL":{
				"en":"Logic unit (ENTER to cancel): ",
				"pt":"Unidade lógica (ENTER para cancelar): ",
				"es":"Unidad lógica (ENTER para cancelar): ",
				"tl":"ngu'wI' QapwI' (ENTER qIlmeH): "
			},
			"print_name":{
				"en":"Printer name: ",
				"pt":"Nome da impressora: ",
				"es":"Nombre de la impresora: ",
				"tl":"pongDaj ghItlhDe'wI': "
			},
			"file_name":{
				"en":"File name: ",
				"pt":"Nome do arquivo: ",
				"es":"Nombre del archivo: ",
				"tl":"pongDaj navDe'wI: "
			},
			"op_mode":{
				"en":"Operation mode -> read (l) or write (e): ",
				"pt":"Modo de operação -> leitura (l) ou escrita (e): ",
				"es":"Modo de operación -> lectura (l) o escritura (e): ",
				"tl":"QapwI' Qap -> laD (l) qoj ghItlh (e): "
			},
			"dev_add":{
				"en":"Device added (Type: %s - Logic Unit: %s)",
				"pt":"Dispositivo adicionado (Tipo: %s - Unidade Lógica: %s)",
				"es":"Dispositivo adicionado (Tipo: %s - Unidad Lógica: %s)",
				"tl":"chelta' jan (Segh: %s - ngu'wI' QapwI': %s)"
			},
			"inv_val":{
				"en":"Invalid value",
				"pt":"Valor inválido",
				"es":"Valor inválido",
				"tl":"mI' Hatlu'"
			},
			"mult_par":{
				"en":"More values given than parameters",
				"pt":"Mais valores passados que parâmetros",
				"es":"Mas valores pasados que parámetros",
				"tl":"nobta' mI' law' De'Wa'DIch mI' puS"
			},
			"ini_addr":{
				"en":"Inform initial address: ",
				"pt":"Informe o endereco inicial: ",
				"es":"Informa la posición inicial: ",
				"tl":"wa'DIch qawHaqDaq yI'noblu': "
			},
			"fin_addr":{
				"en":"Inform final address: ",
				"pt":"Informe o endereco final: ",
				"es":"Informa la posición final: ",
				"tl":"Qav qawHaqDaq yI'noblu': "
			},
			"end":{
				"en":"Ended terminal",
				"pt":"Terminal encerrado",
				"es":"Terminal cerrado",
				"tl":"rInta' jIH"
			},
			"no_file":{
				"en":"File does not exist",
				"pt":"O arquivo não existe",
				"es":"Él archivo no existe",
				"tl":""
			}
		}
	def __call__(self, title, args=()):
		return self.message[title][self.language] %(args)
	def presentation(self):
		print("Hi, I'm C-3PO, human-cyborg relations, I'm fluent in over 6 million forms os communication.")
	def fluencies(self):
		print("Up to now, I can only translate the following languages:")
		for lg in self.message["languages"]:
			print("\t"+self.message["languages"][lg]+"("+lg+")")