import asyncio #Biblioteca asincronica
from telethon import TelegramClient, events, sync, types #Biblioteca para trabajar con la API de Telegram
from telethon import functions #Lo mismo de arriba
from telethon.tl.types import * #Lo mismo de arriba x2 si tienes curiosidad de como funciona lee la documentacion en la web, googlea telethon api
import pickle #La biblioteca para serializar cosas en python

#Usa your tus propios datos de my.telegram.org
api_id = "REEMPLAZAR CON TUS DATOS"
api_hash = 'REEMPLAZAR CON TUS DATOS'
bot_token = "REEMPLAZAR CON TUS DATOS" # este dato te lo da botFather cuando creas el bot nuevo
client = TelegramClient("bot",api_id,api_hash).start(bot_token=bot_token) #inicia la secion del bot


print("Iniciando") #un print de control

lista=[] #lista de los mensajes de los usuarios

cartas=[] #la lista de cartas para el 14 de febrero


##### REMPLAZA CON TUS DATOS ######
adm="" #el @ del administrador o a la persona que se le enviaran los mensajes
adm_id=00000000 #el id del administrador, es un numero, no un string

#fichero=open("cartas.txt","wb")   #esta funcion esta comentada porque solo hay que activarla una vez para que cree la archivo, luego se puede comentar de nuevo
#pickle.dump(cartas,fichero)   #asi se serializa un objeto en python
#fichero.close()


#Mensaje de ayuda que sale en el help
ayuda="1-Para enviar mensajes al canal se usan los siguientes comandos: \n/enviar 'mensaje a enviar'\n*Ejemplo: \n/enviar Te tengo un chisme nuevo \n2-Para enviar una cancion 🎧 o foto 📸 se utiliza el mismo comando, ademas se puede responder una foto o cancion con el comando /enviar *'Mensaje a enviar' \n*Ejemplo: \n(responde una foto o cancion y luego escribe en el chat) \n/enviar *Aqui mando una cancion para mi persona especial \n3-Tambien puedes enviar encuestas solo creandola en el chat del bot. \n4-Para enviar una carta al buzon para el 14 de febrero se usa el comando /carta seguido del texto de la carta y al final 'Para:' tal persona\n*Ejemplo:\n/carta Hola, seguro no te esperabas recibir una carta por aqui, te quiero mucho y estoy enamorado de ti. Para:Fulanita de Matematica\n5-Si tienes alguna queja o sugerencia usa el comando /feedback, funciona igual que /enviar\n6-Para unirte al canal usa el comando /canal"

#Funcion principal del bot, esta funcion se activa cada vez que le llega un mensaje al bot, sea cual sea este lo escucha y recibe un objeto event con todos los datos
@client.on(events.NewMessage)
async def handle_new_message(event):
    sender = await event.get_sender()  #IMPORTANTE: el await es para la asincronidad del bot, se debe poner adelante de cada funcion que se vaya a hacer
    chat = await event.get_chat() #Estas primeras cosas es para guardar el enviador, el chat de donde se envia y el mensaje, excepto el mensaje todo lo demas son objetos especiales de la biblioteca telethon
    mesage=event.message.message
    canal=0000000000 #este es el id del canal a donde envia los mensajes, remplaza con tus datos, es un numero, no un string
    chanel=await client.get_entity(PeerChannel(canal)) #esto es para obtener la identidad del canal a donde se va a enviar los mensajes, es un objeto de la biblioteca
    
    if(mesage=="/help"): #para cuando alguien le escribe /help al bot, automaticamente le envia el mensaje de ayuda
        await client.send_message(chat, message=ayuda) #la funcion send_message requiere primero el chat donde se va a mandar el mensaje y luego el mensaje
        
    elif(mesage[0:8] == "/enviar "): #para cuando es el comando /enviar
        if(event.message.media): #primero se ve si es un archivo(foto o cancion)
            if isinstance(event.message.media, MessageMediaPhoto): #para las fotos, si el mensaje contiene multimedia y esta multimedia es una foto:
                index=mesage.find(" ")
                text=mesage[index+1:]
                text=text.replace("pinga","p*nga")        ### Un mini filtro para las palabrotas 
                text=text.replace("cojone","coj*ne")
                text=text.replace("bollo","b*llo")
                text=text.replace("negga","n*gga")
                text=text.replace("singao","s*ngao")
                text=text.replace("singar","s*ngar")
                await client.send_message(adm, file=event.message.media.photo, message=text) # esto envia el mensaje al administrador por medio del mismo bot, este send_message tiene la diferencia que ademas va a mandar un archivo
                await event.reply("Foto y mensaje enviado al administrador 🚀 si es aprobado se enviara al canal 😉") #a diferencia del send_message, el event.reply solo necesita un texto para responder al evento, este mensaje respondera el mensaje que se le envio
                user={"id":event.sender.id,"mess":text} #crea un diccionario con el id del usuario y el mensaje que envio
                lista.append(user) # y lo guarda en esta lista
             
             #Esto es lo mismo pero con canciones, realmente accepta cualquier tipo de documentos, desde archivos hasta strickers
            elif isinstance(event.message.media, MessageMediaDocument):
                index=mesage.find(" ")
                text=mesage[index+1:]
                text=text.replace("pinga","p*nga")
                text=text.replace("cojone","coj*ne")
                text=text.replace("bollo","b*llo")
                text=text.replace("negga","n*gga")
                text=text.replace("singao","s*ngao")
                text=text.replace("singar","s*ngar")
                await client.send_message(adm, file=event.message.media.document, message=text)
                await event.reply("Cancion y mensaje enviado al administrador 🚀 si es aprobado se enviara al canal 😉")
                user={"id":event.sender.id,"mess":text}
                lista.append(user)
        
        elif(mesage[0:9] == "/enviar *" and event.message.reply_to): #este es para el comando de los reenvios
                reply_to_msg_id = event.message.reply_to.reply_to_msg_id #se toma el id del mensaje original en el chat
                reply_to_peer_id = event.message.reply_to.reply_to_peer_id #se toma el id del mensaje que lo respondio
                original_message = await client.get_messages(reply_to_peer_id, ids=reply_to_msg_id) #y se obtiene el mensaje original mediante este metodo que retorna la lista de mensaje del chat entre parametros, en plan una lista de 10 mensajes, bueno dame el mensaje entre la 9na y 10ma poscion, te va a dar el 9no mensaje, como objeto message
                text=original_message.message #tomamos el texto original
                index=mesage.find("*")
                if(original_message.media): #como siempre se ve primero es un mensaje con multimedia
                    if isinstance(original_message.media, MessageMediaPhoto):
                        await client.send_message(adm, file=original_message.media.photo, message=mesage[index+1:])
                        await event.reply("Foto y mensaje enviado al administrador 🚀 si es aprobado se enviara al canal 😉")
                        user={"id":event.sender.id,"mess":mesage[index+1:]}
                        lista.append(user)
                    elif isinstance(original_message.media, MessageMediaDocument):
                        await client.send_message(adm, file=original_message.media.document, message=mesage[index+1:])
                        await event.reply("Cancion y mensaje enviado al administrador 🚀 si es aprobado se enviara al canal 😉")
                        user={"id":event.sender.id,"mess":mesage[index+1:]}
                        lista.append(user)
                else: #este else es por si no es multimedia, pos es de texto
                    await client.send_message(adm, text)
                    await event.reply("Mensaje enviado al administrador 🚀, si es aprobado se enviara al canal 😉")
                    user={"id":event.sender.id,"mess":text}
                    lista.append(user)
             
        else:  #y este es el else del if del principio, si no es multimedia es texto
            index=mesage.find(" ")
            text=mesage[index+1:]
            text=text.replace("pinga","p*nga")
            text=text.replace("cojone","coj*ne")
            text=text.replace("bollo","b*llo")
            text=text.replace("negga","n*gga")
            text=text.replace("singao","s*ngao")
            text=text.replace("singar","s*ngar")
            await client.send_message(adm, text)
            await event.reply("Mensaje enviado al administrador 🚀, si es aprobado se enviara al canal 😉")
            user={"id":event.sender.id,"mess":text}
            lista.append(user)
             
             
    elif(event.message.poll):  #este es el de la encuesta, directamente si el mensaje es una encuesta la envia al chat del administrador
        await event.reply("Encuesta recibida y enviada al administrador 🚀 , si es aprobada se enviara al canal 😉")
        await client.send_message(adm , file=event.poll , message="" ) #si, se envia la encuesta como archivo, me tomo todo un dia averiguar eso
        
    elif(mesage[0:7]== "/carta "): #la funcion de la carta que se activa con el comando /carta
        index=mesage.find("Para:") #si no encuentra el Para: no funciona y dara error
        if(index>20): #la carta no puede ser corta
            fichero=open("cartas.txt","rb")
            cartas=pickle.load(fichero) #se carga el archivo binario de las cartas y de el la lista
            fichero.close()
            cartas.append(mesage[7:]) #se mete la carta en la lista
            fichero2=open("cartas.txt","wb")
            pickle.dump(cartas,fichero2) #y se vuelve a guardar, como quien abre una caja, mete algo y la vuelve a guardar
            fichero2.close()
            await event.reply("Carta enviada 🚀, se guardara hasta el 14 de febrero y luego sera abierta")
        else:
            await event.reply("Texto de carta muy corto o no se ha encontrado el 'Para:'")
            
    elif(mesage == "/abrir" and sender.id == adm_id): #El comando abrir que solo funciona si lo manda el administrador
        await event.reply("Se ha abierto el buzon, se enviaran todas las cartas al canal")
        fichero=open("cartas.txt","rb")
        cartas=pickle.load(fichero) #carga la lista de cartas
        fichero.close()
        for carta in cartas:
            await client.send_message(chanel, message=carta) #las envia una a una al canal
            
    elif(mesage=="/num"): #esto es para saber la cantidad de cartas que hay en el buzon
        fichero=open("cartas.txt","rb")
        cartas=pickle.load(fichero) #se carga, se cuentan y se muestra la cantidad
        fichero.close()
        await event.reply("En este momento se encuentran " + str(len(cartas)) + " cartas en el buzon")
            
    elif(mesage=="/start"): #el comando /start que es el mensaje de bienvenida al bot
        await client.send_message(chat,"Hola! escribe /help para obtener ayuda de como enviar mensajes al canal")
        
    elif(mesage=="/canal"): #el comando /canal que te envia el link del canal para que los usuarios se unan
        await event.reply("Link del canal de Secretos y Confesiones 🤫: https://t.me/**sustituir_por_otro**")
        
    elif(mesage=="/done" and event.message.reply_to and sender.id == adm_id): #el comando /done es para aprobar los mensajes que le llegan al adm, este se activa cuando respondes el mensaje a aprobar con el /done
        reply_to_msg_id = event.message.reply_to.reply_to_msg_id
        reply_to_peer_id = event.message.reply_to.reply_to_peer_id
        original_message = await client.get_messages(reply_to_peer_id, ids=reply_to_msg_id) #se busca el mensaje a aprobar, ya que como es reenviado se debe hacer de este modo
        text=original_message.message #el texto del mensaje original
        if(original_message.media): #si el mensaje trae multimedia:
            if isinstance(original_message.media, MessageMediaPhoto): #si es foto
                await client.send_message(chanel , file=original_message.media.photo , message=text)
                await event.reply("Foto enviada al canal")
            elif isinstance(original_message.media, MessageMediaDocument): #si es un documento
                await client.send_message(chanel , file=original_message.media.document , message=text)
                await event.reply("Cancion enviada al canal")
            elif (original_message.poll):
                await client.send_message(chanel, file=original_message.poll , message="") #si es una encuesta
                await event.reply("Encuesta enviada al canal")
        else:
            await client.send_message(chanel,original_message.message) #si es un mensaje normal de texto
            await event.reply("Mensaje enviado al canal")
        
    elif(mesage[0:10] == "/feedback "): #el comando del feedback para que los usuarios puedan retroalimentar el canal con ideas y tal
        index=mesage.find(" ")
        text="Mensaje de feedback: "
        text=text + mesage[index+1:]
        await client.send_message(adm, text )
        await event.reply("Mensaje enviado al administrador, gracias por la sugerencia 😁")
        
    elif(mesage[0:4] == "/no " and event.message.reply_to and sender.id == adm_id ): #este es el comando que deniega un mensaje que llega, ya sabes, respondiendo con /no el mensaje y luego escribiendo un motivo
        reply_to_msg_id = event.message.reply_to.reply_to_msg_id
        reply_to_peer_id = event.message.reply_to.reply_to_peer_id
        original_message = await client.get_messages(reply_to_peer_id, ids=reply_to_msg_id) #se busca el mensaje que se responde
        text=original_message.message #se toma el texto
        index=mesage.find(" ")
        mensage="El mensaje: '" + text + "' no ha sido enviado porque: " + mesage[index+1:] #esto es una plantilla a enviar
        for user in lista: #va a buscar en la lista de mensajes
            if(user["mess"]==text): # el mensaje que denegaste
                id=user["id"]
                await client.send_message(id,mensage) # y si lo encuentra va a enviar la plantilla de arriba al usuario que lo escribio, de esa forma se evita que el administrador conozca quien lo envia
                await event.reply("Mensaje enviado")
                lista.remove(user) # y al final elimina ese mensaje de la lista de mensajes
        
    else: #en el caso de que el texto del mensaje no sea ningun comando:
        if not isinstance(chat,Channel): #mientras el chat donde recibe el mensaje no sea un canal:
            await client.send_message(chat,"Formato del mensaje incorrecto, si tiene dudas presione /help") #oye fijate que escribes
         
with client: #y para finalizar el bot estara carriendo indefinidamente :)
    client.run_until_disconnected()
    
    #Este es el codigo para crear un bot identico al bot de chismes de la facultad, un gran poder conlleva una gran responsabilidad, por favor usalo sabiamente
    
    ########### GRACIAS POR TODO EL APOYO QUE RECIBIO EL CANAL, OS QUIERO A TODOS, MAñANA 16 DE FEBRERO HABRA OTRA SORPRESA ###########


