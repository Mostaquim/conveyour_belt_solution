import random


class Conveyor:
    def __init__(self, steps, belt_length, worker_time_required, slot_time):
        self.steps = steps
        self.worker_time_required = worker_time_required
        self.worker_group = Conveyor.get_workers(belt_length, slot_time, worker_time_required)
        self.belt_length = belt_length
        self.belt_slots = Conveyor.create_belt_slot(belt_length)
        self.report = Report(steps)
    @staticmethod
    def create_belt_slot(belt_length):
        slots = []
        for i in range(belt_length):
            slots.append(Conveyor.product_generation())
        return slots
    @staticmethod
    def get_workers(slots, slot_time, time_required):
        workerGroup = []
        for i in range(slots):
            workerGroup.append(WorkerPair(Worker('L%i' %i, time_required), Worker('R%i' %i, time_required) , slot_time ) )
        return workerGroup

    @staticmethod
    def product_generation():
        return random.choice(['A','B',''])

    def run(self):
        print('\n STARTING CONVEYOUR BELT')
        for i in range(self.steps):
            print('\n __________STEP NO %i______________' % i)
            print(self.belt_slots)
            for j in range(self.belt_length):
                print('\n ====Belt NO %i==== Product %s ===' % (j, self.belt_slots[j]))
                status = self.worker_group[j].run(self.belt_slots[j])
                if status == 'product':
                    self.belt_slots[j] = 'P'
                elif status == 'taken':
                    self.belt_slots[j] = ''
            self.report.add(self.belt_slots[-1])
            self.belt_slots = [Conveyor.product_generation()] + self.belt_slots[:-1]
        self.report.generate()

class Conveyor_slot:
    def __init__(self,product):
        self.product = product

class WorkerPair:
    def __init__(self, leftworker, rightworker, slot_time):
        self.leftworker = leftworker
        self.rightworker = rightworker
        self.busyworker = None
        self.slot_time = slot_time
        self.active_worker = ''
    @staticmethod
    def diceroll():
        return random.choice(['leftworker','rightworker'])

    @staticmethod
    def get_opposite(worker):
        if worker == 'leftworker':
            return 'rightworker'
        else:
            return 'leftworker'

    def run(self, slot):
        self.leftworker.notify(self.slot_time)
        self.rightworker.notify(self.slot_time)
        self.active_wroker = self.diceroll()
        status = getattr(self, self.active_wroker).run(slot)
        
        if status == 'pass':
            opposite_worker = self.get_opposite(self.active_worker)
            print('Passing to %s' % opposite_worker)
            getattr(self, opposite_worker).run(slot)
            return ''
        else:
            return status
class Report:
    def __init__(self,steps):
        self.products_created = 0
        self.wasted_material = 0
        self.steps = steps
    def add(self, val):
        if val == 'P':
            self.products_created += 1
        elif val == 'A' or val =='B':
            self.wasted_material += 1

    def generate(self):
        print('%s Products generated' % self.products_created)
        print('%s Wasted Materials' % self.wasted_material)
class Worker:
    def __init__(self, name, time_required ):
        self.name = name
        self.time_required = time_required
        self.storage = []
        self.busy_time = 0
        self.has_product = 0
    def notify(self, slot_time):
        if self.busy_time > 0:
            self.busy_time -= slot_time
        if self.busy_time == 0 and len(self.storage) == 2:
            self.has_product = 1

    def run(self, slot):
        if self.has_product == 1:
            if slot == '':
                self.storage = []
                print('%s worker placed completed item %s' % (self.name, slot))
                self.has_product = 0
                return 'product'
            else:
                return 'pass'
        else:
            if slot == '' or slot == 'P':
                return ''
            if self.busy_time <=0:
                if slot in self.storage:
                    return 'pass'
                else:
                    print('%s worker picked item %s' % (self.name, slot))
                    self.storage.append(slot)
                    return 'taken'
                if len(self.storage) == 2 :
                    print('%s worker started assembly' % self.name)
                    self.busy_time = self.time_required
            else:
                return 'pass'
        
        
        
Conveyor(100, 3, 2, 2).run()