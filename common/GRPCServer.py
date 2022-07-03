from concurrent import futures

import grpc

class GRPCServer:
  def __init__(self, max_workers=10):
    self.server = grpc.server(futures.ThreadPoolExecutor(max_workers))

  def register(self, service_class, stub, stub_grpc, service_class_args=()):
    Service = service_factory(service_class, stub, stub_grpc)
    methods_list = [method for method in dir(service_class) if method.startswith("__") is False]
    for method in methods_list:
      implementation = method_factory(service_class.__name__, method)
      setattr(Service, method, implementation)
    exec(f'stub_grpc.add_{service_class.__name__}Servicer_to_server(Service(service_class, stub, stub_grpc, service_class_args), self.server)')
  
  def listen(self, ip='0.0.0.0', port=3000):
    self.server.add_insecure_port(ip + ':' + str(port))
    self.server.start()
    self.server.wait_for_termination()
  
  def stop(self, grace=0):
    self.server.stop(grace)

def service_factory(service_class, stub, stub_grpc):
  code = '''
class Generated{name}Service(stub_grpc.{name}Servicer):
  def __init__(self, base_service, stub, stub_grpc, service_class_args):
    self.base_service = base_service(*service_class_args)
    self.stub = stub
    self.stub_grpc = stub_grpc
'''.format(name=service_class.__name__)
  exec(code)
  Class = eval('Generated{name}Service'.format(name=service_class.__name__))
  return Class

def method_factory(class_name, method_name):
  code = f'''
def generated_{class_name}_{method_name}(self, request, context):
  request_params = {{ }}
  request_vars = [key for key in dir(request) if key[0].islower()]
  for var in request_vars:
    request_params[var] = getattr(request, var)
  response = self.base_service.{method_name}(**request_params)
  if not type(response) == type({{}}):
    response = {{}} 
  return self.stub.{method_name}Reply(**response)
'''
  exec(code)
  method = eval('generated_{class_name}_{method_name}'.format(class_name=class_name, method_name=method_name))
  return method
