import grpc

class GRPCClient:
  def __init__(self, ip, port):
    self.channel = grpc.insecure_channel(ip + ':' + str(port))
  
  def get_provider(self, service_name, stub, stub_grpc):
    service_stub = eval(f'stub_grpc.{service_name}Stub(self.channel)')
    Provider = class_factory(service_stub)
    methods_list = [method for method in dir(service_stub) if method.startswith("_") is False]
    for method in methods_list:
      implementation = method_factory(service_stub, method)
      setattr(Provider, method, implementation)
    return Provider(service_stub, stub)

def class_factory(service):
  code = f'''
class Generated{service.__class__.__name__}:
  def __init__(self, service, stub):
    self.base_service = service
    self.stub = stub
'''
  exec(code)
  Class = eval(f'Generated{service.__class__.__name__}')
  return Class

def method_factory(service, method_name):
  code = f'''
def generated_{service.__class__.__name__}_{method_name}(self, **args):
  return self.base_service.{method_name}(self.stub.{method_name}Params(**args))
'''
  exec(code)
  method = eval(f'generated_{service.__class__.__name__}_{method_name}')
  return method
