from anime_crawler import Engine, StopConditions, RequestsGenerator


s = StopConditions()
s.add_stop_condition(timerange="16:32-16:33")
# print(s.valid())
Engine.run(RequestsGenerator, s)
