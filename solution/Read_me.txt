#В папке input - аудио, что было приложено 

#test_mono_r2.wav и test_mono_r05.wav - растяжение и сжатие в 2 раза 

#Запуск скрипта: cd solution./run.sh argvs, либо без cd solution если зашли в папку

#argvs - аргументы скрипта: 1) input_path.wav - путь к исходному файлу, 2) output_path.wav - куда запишем аудио

#3) r - коэффициент удлиннения

#Пример запуска:
	cd solution&&./run.sh test_mono_r05.wav output.wav 2
	cd solution&&./run.sh input/test_mono.wav output.wav 0.2