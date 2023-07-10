#!/usr/bin/env python3
'''
insertTransDistro.py is a python script to insert minority language translations 
in a Linux distro, where the majority of the distro will stay in another language.
It was created to insert Aymara phrases in the Cinnamon menu of PluriOS, while 
leaving the rest of the system in Spanish, but it can be used by any language. 

USAGE:   
python3 insertTransDistro.py [-v] TRANSLATIONS-FILE [TARGET-DIRECTORY]

OPTIONS:
-d CHAR, --delimiter CHAR           
                  The character separating fields in the CSV file. By default
                  set to ; (semicolon).

-q CHAR, --quote-char CHAR  
                  The character used to quote text in fields in the CSV file. By
                  default set to " (double quotation mark).
                  
-s DIR, --source-dir DIR
                  The directory where the source code for programs is downloaded
                  to get the PO translation files. If the program has already 
                  been downloaded, it won't be downloaded again. By default set
                  to the "source" directory in the current directory.
                  
-l LANG, --language LANG
                  ISO language code for the language which is being replaced, 
                  such as "es" for Spanish, "fr" for French, etc. 
                  
 
-v, --verbose     List each of the files which has been modified. 

-h, --help        Show help for this script.

          
WHERE:
TRANSLATIONS-FILE A comma-separated-value (CSV) file containing translations to 
                  be inserted in the Linux distro. By default the fields are 
                  delimited by ; (semicolons) and use " (double quotation marks)
                  to quote the text in a field, but these values can be set as 
                  options.

TARGET-DIRECTORY  Optional. Directory where the changed files will be stored.
                  If not specified, then the files in the existing Linux system
                  will be overwritten and this script should be executed with 
                  su or sudo.    

The spreadsheet file should contain the following columns:

/path/to/file   | Phrase to find | Replacement translation | Fix phrase       |
----------------|----------------|-------------------------|------------------|
path1           | phrase1        | translation1            | fix-phrase1       |
path2           | phrase2        | translation2            | fix-phrase2       |
...
 
The first row in the spreadsheet consists of headers and will be ignored and all
subsequent rows will be inserted in the Linux distro. The first column contains
the path to a .mo, .desktop or .directory file where the translation will be 
inserted. The second column is the phrase to search for and the third column is
the translation to insert in its place. The fourth column is optional and is 
used to replace the "Phrase to find". If preceded by "PO: ", it inserts a new
phrase in the PO translation file.

Example: 
In PluriOS, the "Phrase to find" is in Spanish, the "Replacement Translation" is
in Aymara and the "PO phrase to add" is the original English.

Autor: Amos Batto <amosbatto@yahoo.com>
Versión: 0.1 (2022-09-01)
Licencia: GPL 3.0 o después
'''
 
import shutil, os, os.path, sys, argparse, pathlib, csv

# Contador de archivos de lengua copiado de DIR_LANG a PluriOS
FilesCopied = 0
 
def main ():
	global FilesCopied
	
	parser = argparse.ArgumentParser(
		description = """
		insertTransDistro.py is a python script to insert minority language 
		translations in a Linux distro, where the majority of the distro 
		will stay in another language. It was created to insert Aymara phrases 
		in the Cinnamon menu of PluriOS, while leaving the rest of the system 
		in Spanish, but it can be used by any language.
		"""
	)
	parser.add_argument(
		"-v", "--verbose",
		action = 'store_true', #indicates a flag without an argument  
		help = "List each of the files which has been modified."
	)
	parser.add_argument(
		"-d", "--delimiter",
		default = ";",
		help = "The character separating fields in the CSV file. By default, set "\
			"to ; (semicolon).",
	)
	parser.add_argument(
		"-q", "--quote-char",
		default = '"',
		help = 'The character used to quote text in fields in the CSV file. '\
			'By default set to " (double quotation mark).'
	)
	parser.add_argument(
		"-s", "--source-dir",
		default = "source",
		help = """The directory where the source code for programs is downloaded
			to get the PO translation files. If the program has already 
			been downloaded, it won't be downloaded again. By default set
			to the "source" directory in the current directory."""
	)
	parser.add_argument(
		"-r", "--replace-lang", 
		default = "es",
		help = """ISO language code for the language which is being replaced,
			which by default is "es" for Spanish.""" 
	parser.add_argument(
		'TRANSLATIONS-FILE', 
		type = pathlib.Path,
		help = """A comma-separated value (CSV) file containing translations to 
			be inserted in the Linux distro."""
	)
	parser.add_argument(
		'TARGET-DIRECTORY',
		nargs = '?', 
		type  = pathlib.Path,
		help  = """Optional. Directory where the changed files will be stored.
			If not specified, then the files in the existing Linux system
			will be overwritten and this script should be executed with 
			su or sudo."""
	)
	 
	args = parser.parse_args()
	transFileName = args['TRANSLATIONS-FILE']
	targetDir = args['TARGET-DIRECTORY']
	
	if not os.exists(transFileName):
		print(f"Translation file '{transFile}' doesn't exist or doesn't have permission to open.")
		parser.print_help() 
		exit(1);
	
	with open(transFileName, newline='') as transFile:
		transReader = csv.DictReader(csvfile, delimiter=args.delimiter, quotechar=args.quote_char, 
			newline='', fieldnames=('path', 'findPhrase', 'translation', 'fixPhrase'))
		
		#skip the first row which is assumed to be a header row
		next(transReader)
		
		for row in transReader:
			
			#skip rows whose path field is empty
			if not row.path or row.path.strip() == '':
				continue
			
			basename = os.path.basename(row.path)
			ext = pathlib.Path(basename).suffix
			
			if targetDir:
				
				
				
			
			 
		
		
		
	
	if (targetDir):
		os.makedirs(targetDir, exist_ok=True)
	
	
			o startDir = os.path.join(args.source_dir, args.language)
		FilesCopied = 0  
		copyDir(startDir, args)
		print (f"{FilesCopied} files had phrases inserted.\n"
			"To see the changes either refresh Cinnamon or  necesario hacer logout o refrescar Cinnamon para ver los cambios."
		)
	elif (args.info):
		os.system("lsb_release -a")
		os.system("uname -a")
		
		if (args.verbose):
			os.system("lshw")
	else:
		parser.print_help()


def copyDir (pathDir, args):
	"""Función recursiva para copiar un directorio de archivos de lengua al sistema de PluriOS
	
	sPath: El directorio actual de donde está copiando los archivos. EJ: /usr/share/plurios-languages/ay/usr/share
	args: Los argumentos pasados a script al inicio.
	"""
	global FilesCopied
	
	for sChild in os.listdir(pathDir):                
		sChildPath = os.path.join(pathDir, sChild)
		baseDir = os.path.join(args.source_dir, args.language)
		sTargetPath = sChildPath[ len(baseDir) : ]
		
		if (args.verbose):
			print (sTargetPath)
		
		try:
			if os.path.isfile(sChildPath):
				if os.path.exists(sTargetPath) and os.path.isfile(sTargetPath):
					os.remove(sTargetPath)
				
				shutil.copy2(sChildPath, sTargetPath);
				FilesCopied += 1
				# copy2() no copia el dueño y grupo, pero debe copiar como root:
				#st = os.stat(sChildPath)
				#os.chown(sTargetPath, st.st_uid, st.st_gid)
				
			elif os.path.isdir(sChildPath):
				if not os.path.exists(sTargetPath) or not os.path.isdir(sTargetPath):
					st = os.stat(sChildPath)
					os.mkdir(sTargetPath, st.st_mode) 
				
				copyDir(sChildPath, args)
		except PermissionError:
			exit(f"No tiene permisos para escribir los archivos de lengua.\n"
				f"Deberia ejecutar: sudo plurios -l {args.language}")


if __name__ == "__main__":
    main()

