# plurios-languages

plurios-languages is a project to translate the [PluriOS](https://plurios.openit.dev) Linux distribution 
into native languages of Bolivia. PluriOS is based on [Ubuntu Cinnamon Remix](https://ubuntucinnamon.org/) 
20.04 LTS “Focal Fossa”, but we hope that plurios-languages can be packaged, 
so it can be installed in other distros which offer the Cinnamon interface.  

## The challenge
To fully localize Linux in another language requires translating over million
words. LibreOffice alone contains roughly 300,000 words. OpenIT offered us
a small fund to translate PluriOS's Cinnamon interface and main menu into Aymara, 
Quechua and Guarani, but that only consists of roughly 11,000 words for each 
language.

If we switch the system language to Aymara, Quechua or Guarani, we will have a
problem, because the rest of the software the system won't have a translation, 
so it will default to English, which is a language which very few speakers of 
Bolivian native languages know. 

Another problem is that these languages often don't have locale files. For example, 
there is a locale for `ay_PE` (aymara from Perú), but not for `ay` (aymara in general) 
or `ay_BO` (aymara from Bolivia). GNOME gets its locales from clib, so we would
have to file issue reports with clib to get new locales created. 

Another challange is that we need the ability to switch the interface from the
native language to Spanish and back again. Many speakers of native languages have
limited ability to read in their language, whereas they are trained to read and write
in Spanish (or another dominant language such as English, Portuguese or French). 
Often the people who have more ability in the native language have to rely on
non-speakers for help when using the computer, so it is important that be possible
to easily switch the language. 

In addition, translating the Linux interface into a native language often involves 
creating neologisms or new terms to cover the new terminology for the technology. 
In Aymara, we had to create dozens of neologisms for terms such as "file" (*wayaqa*), 
"folder" (*q'ipi*), "document" (*qillqa-wayaqa*), table (*uyu-uyu*), "energy" (ch'ama), 
"touchpad" (wikuchiri pampa), "package" (*q'ipicha*), "font" (*qillqa kasta*), "privacy" 
(*sapa jaqinkirina*), "network" (*llika*), "internet" (*llikapura*), etc. Plus, we 
borrowed dozens of technical words from Spanish, which we rephoneticized in the fro
Aymara alphabet, such as "aplicación" (*aplikasiyuna*), "ventana" (*wintana*), 
"computadora" (*kumputarura*), "escritorio" (*iskrituryu*), "teclado" (*tiklaru*), 
etc. Sometimes it was possible to include the Spanish translation in parentheses
to let users know what a neologism or borrowed term means. However, it is often
necessary to switch the interface between Aymara and Spanish to discover the meaning
of unfamiliar terms.

## Our solution
Since we didn't want to use most of our software in English nor wait for new locales to be 
created, we decided to use the existing locale, which in our case is `es_BO` 
(Spanish from Bolivia) and create language files in native languages for that locale.
In other words, the system still operates in the `es_BO` locale, but the
Spanish translation files for the Cinnamon interface and the main menu have been 
replaced with native language translation files. 

For the user, the Cinnamon interface appears Aymara (and in Quechua and Guaraní 
in the future when we start translating in those languages), but the rest of the
programs appear in Spanish. 

Unfortunately, the package managers in Linux distros do not allow packages
to over-write the files from other packages. For example, if we want to over-write
Cinnamon's Spanish translation files with Aymara, then we need to uninstall the
existing `cinammon-l10n` package and install our own custom package in its place 
with the Spanish text replaced by Aymara text in files with the same filenames.
This works if dealing with replacig just one or two packages, but when we tried 
to replace PluriOS's Spanish menu with an Aymara menu, we found that we needed to
replace over 150 files found in roughly 100 different packages.

We decided that the best solution was to include all the translation files in one
package and store them in a place in the file system where they wouldn't interfere
with other packages (namely `/usr/share/plurios-languages/{lang}/`) and then create 
a python script, which we named "plurios", that could be executed with root permissions
to overwrite the existing language files to switch the language of the interface.

We added this option to the main menu, so users could easily execute the script. 
Unfortunately, Cinnamon needs to be refreshed after switching the language files 
(or the user has to manually logout and login again) in order to display the new 
language in some parts of the main menu, it isn't a seamless transition between
languages. 

We hope to also add the Quechua and Guarani translations in the same way to plurios-languages
when we finish the translations.

## Using plurios-languages

If using a Debian-based distro with the Cinnamon interface, download the 
`plurios-languages_0.1-0_all.deb` package and install it:

`sudo dpkg -i plurios-languages_0.1-0_all.deb`

Then, run the `plurios` script to install the language files for either Aymara ("ay")
or Spanish ("es"):

`sudo plurios -l ay`

or:

`sudo plurios -l es`

Some of the changes to the language will immediately be visible in the interface 
(such as the `.desktop` files), but other changes (such as the `.mo` files) will
only be displayed by logging out of Cinnamon and then logging in again. Another option
is to refresh the Cinnamon interface by simultaneously pressing the ALT + F2 keys.
In the dialog box that appears, enter `r` and press ENTER. A few seconds later,
Cinnamon will reappear with the updated language.

To see a list of all the files and directories that are changed, use the `-v` option
for more verbose output. 

`sudo plurios -v -l ay`


To see information about the system, use the `-i` option:

`plurios -i`

To also see information about the system's hardware, include the `-v` option:

`sudo plurios -v -i`

For help using the `plurios` script, use the `-h` option:    

`plurios -h`

## Constructing the `plurios-languages` package

To build the `plurios-languages` package, download the `plurios-languages_0.1-0_all` 
directory. Then, issue the following command:

`dpkg-deb --build --root-owner-group plurios-languages_0.1-0_all`

If needing to add additional language files to the package, then they needed to
be added in the location:  
`plurios-languages_{version}-0_all/usr/share/plurios-languages/{lang}/{location-in-file-system}`

For example, if you want to add the file `/usr/share/applications/myapp.desktop`
for Aymara, then it will be placed at:  
`plurios-languages_0.1-0_all/usr/share/plurios-languages/ay/usr/share/applications/myapp.desktop`

If needing to change the text of a `.mo` translation file, first install the `poedit` package.
Then, download the source code for the package that contains the translation file.
For example, if you want to add the Aymara translation for the TuxPaint package, 
download the source code:  
`apt source tuxpaint`
  
Then, open the Spanish translation file with [PoEdit](https://poedit.net) and change the Spanish to Aymara:  
`poedit tuxpaint-0.9.23/po/es.po`

When done editing the PO file, save it in PoEdit to automatically generate the `.mo` file. 
Then copy the `.mo` to the location in the package's file structure, so it will 
be installed in the correct location in the system when the `plurios -l` script is executed.

For example:  
`sudo cp tuxpaint-0.9.23/po/es.mo plurios-languages_0.1-0_all/usr/share/plurios-languages/ay/usr/share/locale/es/LC_MESSAGES/tuxpaint.mo`

If unsure where to place the `.mo` file, install the program's normal package on the
system and then search for its `.mo` file. For example:  
```sudo apt install tuxpaint
sudo find  / -iname tuxpaint.mo```

If unable to find where a phrase is translated, use the `grep` command to find it. 
For example, you see the phrase "My cool app" in the interface, then you search
for its file with this command:  
`sudo grep -r -i "My cool app" /usr/share/`

## License info ##

The `plurios` script has a GPL 3.0 or later license. The language files have the
license of their software project. If unsure which project a language file comes from, 
that information can usually be found by opening the `.desktop` files with a plain text editor
(such as [Geany](https://www.geany.org)) or by examining the `.mo` files with a binary 
file editor (such as [GHex](https://wiki.gnome.org/Apps/Ghex)).

