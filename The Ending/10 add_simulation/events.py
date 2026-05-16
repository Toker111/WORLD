from typing import Callable,Dict,List

class EventBus:
    #创建储存函数地方
    def __init__(self) -> None:
        self._listeners:Dict[str,List[Callable]]={}

    #收录函数
    def subscribe(self,event_type:str,callback:Callable) -> None:  #event_type事件名称 callback 回调(指的是现在不用等会用的函数)
        if not event_type in self._listeners:
            self._listeners[event_type]=[]
        self._listeners[event_type]=[callback]

    def publish(self,event_type:str,data:object=None) -> None:
        if event_type in self._listeners:
            for callback in self._listeners[event_type]:
                callback(data)
