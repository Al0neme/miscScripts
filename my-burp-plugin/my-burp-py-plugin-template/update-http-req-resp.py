# get header value
def get_header_value(header_name, headers):
    for header in headers:
        if header.lower().startswith(header_name.lower()):
            return header.split(":")[1]
    return None

# update header value
def update_headers_value(header_name, header_newvalue, headers):
    for header in headers:
        if header.lower().startswith(header_name.lower()):
            headers.remove(header)
            header = header_name+": "+header_newvalue
            headers.add(header)
            return header
    return None

# handle req and resp
if messageIsRequest:
    # get req data
    req = messageInfo.getRequest()
    req_data = helpers.analyzeRequest(req)
    headers = req_data.getHeaders()
    body = req[req_data.getBodyOffset():].tostring()

    # update param,to handle other param,please replece name 'test'
    for param in req_data.getParameters():
        if param.getName() == 'test':
            # update value,or you can replace 'admin' with other value 
            newParamValue = "admin"
            newParam = helpers.buildParameter(str(param.getName()),newParamValue,param.getType())
            newReqParam = helpers.updateParameter(req,newParam)
            messageInfo.setRequest(newReqParam)

    # update header,to handle other header,please replece name 'User-Agent' and replace value 'fuckagent' 
    req = messageInfo.getRequest()
    req_data = helpers.analyzeRequest(req)
    headers = req_data.getHeaders()
    update_headers_value('User-Agent','fuckagent',headers)
    body = req[req_data.getBodyOffset():].tostring()
    newReq = helpers.buildHttpMessage(headers,body)

    messageInfo.setRequest(newReq)
    # messageInfo.setRequest(newHeader)

else:
    # get resp data
    resp = messageInfo.getResponse()
    resp_data = helpers.analyzeResponse(resp)
    headers = resp_data.getHeaders()
    body = resp[resp_data.getBodyOffset():].tostring()

    # update response data,example header value and body value
    update_headers_value('Server','fuckserver',headers)
    newBody = body+"\n"+"what fuck"
    newResp = helpers.buildHttpMessage(headers,newBody)
    messageInfo.setResponse(newResp)