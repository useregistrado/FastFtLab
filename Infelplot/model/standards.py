def stnd(arg):
    switch={
        'apd':("Apatito de Durango con edades por K-Ar",31.4,0.5,31.9,30.9),
        'apc':("Apatitos y circones de la toba volcanica Fish Canyon con edad por K-Ar",27.9,0.5,28.4,27.4),
        'cmb':("Circones del miembro Buluk con edades por K-Ar",16.4,0.2,14.6,16.2),
        'cdm':("Circones de Dromedary Mountains con edades por K-Ar",98.7,0.6,99.3,98.1),
        'crt':("Circones de la riolita de Tardree con edades por K-Ar",58.7,1.1,59.8,57.6),
        'cvb':("Circones de la toba volcánica Bishop al este de California con edades por K-Ar",74.0,0.6,74.6,73.4)
    }
    return switch.get(arg,"invalid argument")

#la funcion stnd devuelve una tupla de los estandares de minerales, dependiendo del argumento ingresado,
#en las posiciones de la tupla se encuentran organizados los atributos de la siguiente manera:
#("nombre completo del estandard",edad media,± su variacion,edad media mas su variacion,edad media menos u variacion)
