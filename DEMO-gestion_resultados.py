def my_encoding(text):
    c = 13
    cipher = ""
    for char in text:
        char = ord(char)
        if 97 <= char <= 123:
            if c+char < 123:
                cipher += chr((char) + c) 
            elif c+char >= 123:
                cipher += chr((char) - c)
            elif 65 <= char <= 90:
                if c+char < 90:
                     cipher += chr((char) + c) 
                elif c+char >= 90:
                    cipher += chr((char) - c)		
                else: cipher += chr(char)
    return cipher

def my_decoding(list_text):
    c = 13

    final_list = []    
    for item in list_text:
        message=""
        for char in item:
            char = ord(char)
            if 97 <= char <= 122:  # Lowercase letters
                if char - c >= 97:
                    message += chr(char - c)
                else:
                    message += chr(char + 26 - c)
            elif 65 <= char <= 90:  # Uppercase letters
                if char - c >= 65:
                    message += chr(char - c)
                else:
                    message += chr(char + 26 - c)
            else:
                message += chr(char)
        final_list.append(message)  
    return '\n'.join(final_list)




#las lambdas trabajan con json para imprimir salida por consola
import json 


# SIEMPRE SIEMPRE una lambda trabaja con estos dos parámetros: EVENT y CONTEXT

def lambda_handler(event, context): 
    ######################################################################################
    # Codigo que recoge los dos trozos de texto de las lambdas, y alterna línea a línea
    # para obtener el resultado final.
    ######################################################################################
    event = sorted(event, key=lambda x: x['type_lines'], reverse=True)
    
    v_result = []
    # max_lineas = max(len(item['texto_lineas'].splitlines()) for item in event)
    max_lineas = max(len(item['texto_lineas']) for item in event)
    
    v_result = [
        lineas[i] for i in range(max_lineas) for item in event
        # for lineas in [item['texto_lineas'].splitlines()] if i < len(lineas)
        for lineas in [item['texto_lineas']] if i < len(lineas)
    ]          
    text=my_decoding(v_result)
    texto_formateado = text # '\n'.join(text)
    

    ######################################################################################
    ######Aquí generamos código para guardar este resultado como fichero en S3
    ######################################################################################
    import boto3
    from datetime import datetime

    # INICIALIZAMOS CLIENTE S3 y otras variables
    s3 = boto3.client('s3')

    fecha_hoy = datetime.now().strftime('%Y%m%d-%H:%M:%S')
    fichero_salida = "resultado_final_"+f"{fecha_hoy}"+".txt"
    bucket_name = 'aws-training-csw'

    try:
        s3.put_object(
            Bucket=bucket_name,
            Key=fichero_salida,
            Body=texto_formateado
        )
    
    except:
        return {
            'statusCode': -1,
            'body': json.dumps(" error generando fichero S3 pero el resultado es: \n" + texto_formateado)
                }        
    
    ######################################################################################
    ###### FIN DEL CODIGO PARA GRABAR S3
    ######################################################################################
    else:

        return {
            'statusCode': 200,
            'body': json.dumps(" el fichero S3 se llama:"+fichero_salida + " y el resultado es: \n" + texto_formateado)
            }
                