class String:
    START = 'Ciao,\nsono un bot che permette di cercare i canali di @watchanime.\nInizia a digitare il nome di un ' \
            'anime per cercarne il canale'
    ANIME_NOT_FOUND = 'Nessun risultato per "{query}"\nSe pensi si tratti di un errore, segnalalo <a href="{' \
                      'issues_tracker}">qui</a> '
    QUERY_TOO_SHORT = 'Prova con qualcosa di più lungo di tre caratteri'
    MORE_HELP = 'Bot non ufficiale per la ricerca dei canali di @watchanime.\nLa lista viene aggiornata goirnalmente ' \
                'con i dati prelevati da <a href="https://watchfamily.wordpress.com/liste-anime">qui</a>\n\n' \
                '<b>Wildcards ricerca</b>\nE\' possibile sfruttare le calssiche wildcards SQL quando si effettua una ' \
                'ricerca:\n• il carattere <code>%</code> (percentuale) matcha zero o più caratteri qualsiasi\n• il ' \
                'carattere <code>_</code> (underscore) matcha un solo carattere qualsiasi\n\nUna ricerca non ' \
                'restituisce mai più di 96 risultati\n\n' \
                '- <a href="{source_code}">codice sorgente</a>\n- <a href="{issues_tracker}">segnala un problema</a>'
