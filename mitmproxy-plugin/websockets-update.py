from mitmproxy import http

def websocket_message(flow: http.HTTPFlow):
    assert flow.websocket is not None  # make type checker happy
    last_message = flow.websocket.messages[-1]
    if last_message.from_client:
        # get rep data
        print("client init message: "+str(last_message.content,'utf-8'))
        # update messagecontent,or you can update other value with replace '{"auth_user":"123","auth_pass":"123"}'
        messagecontent = b'{"auth_user":"123","auth_pass":"123"}'
        last_message.content = messagecontent
        print("after client update : "+str(messagecontent,'utf-8'))
    else:
        # get resp data
        print("server init message: "+str(last_message.content,'utf-8'))
        # update messagecontent,or you can update other value with replace 'fuckwebsocksts'
        messagecontent = str(last_message.content,'utf-8')+":::\n"+"fuckwebsocksts"
        print("after server update: "+messagecontent)