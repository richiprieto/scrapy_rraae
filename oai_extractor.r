## Libreria
library(OAIHarvester)

## Direccion
baseurl <- "http://rraae.org.ec:8090/oai/request"

## Identificar
oaih_identify(baseurl)

## Listar formatos de la metadata
oaih_list_metadata_formats(baseurl)

## Listar los sets
sets <- oaih_list_sets(baseurl)
sets

## Listar los records en el set "com_0066".
## Escoger el set que desee cambiando el nombre, consultar el nombre en sets
spec <- unlist(sets[sets[, "setName"] == "com_0066", "setSpec"])
x <- oaih_list_records(baseurl, set = spec)

## Extraer la metadata
m <- x[, "metadata"]
m <- oaih_transform(m[lengths(m) > 0L])

## Transformar a dataframe
df=data.frame(m)
df <- apply(df,2,as.character)

## Escribir en un csv
write.csv(df,file = "datos.csv")
