from random import *

def initial_stats():
    stats={}
    stats_name=['ATK','DEF','MAT','MDE','AGI','LUK']
    counter=0
    data=0
    for i in stats_name:
        data=randint(0,4)
        counter+=data
        stats[i]=data
    while counter<10:
        stats[choice(stats_name)]+=1
        counter+=1
    return stats

def prob(p):
    if p>randint(0,100):
        return True
    else:
        return False

class item():
    def __init__(self,name,description='',usage=1):
        self.name=name
        self.usage=usage
        self.description=description
    def use(self):
        if self.usage==0:
            return False
        else:
            self.usage-=1
            return True
    def getDescription(self):
        s=''
        s+='名称：'+self.name+'\n'
        if self.usage>0:
            s+='可用次数：'+self.usage+'\n'
        if self.description!='':
            s+='描述：'+self.description+'\n'
        return s 

class equipment(item):
    def __init__(self,name,stats,allow_list=[],ability={},description=''):
        item.__init__(self,name,description,usage=-1)
        self.stats=stats
        self.allow_list=allow_list
        self.ability=ability
    def getDescription(self):
        stats_name=['ATK','DEF','MAT','MDE','AGI','LUK']
        s=super().getDescription()
        if self.stats!={}:
            s+='属性：\n'
            for i in stats_name:
                if i in self.stats:
                    s+=i+'：'+str(self.stats[i])+'\n'
        s+='可装备位置：'
        for j in self.allow_list:
            s+=j+'，'
        s=s[:-1]
        s+='\n'
        return s

class weapon(equipment):
    def __init__(self,name,ATK,WOA,ability={},description=''):
        equipment.__init__(self,name,{'ATK':ATK},['左臂','右臂'],ability,description)
        #Way Of Attack
        self.WOA=WOA 
    def getDescription(self):
        s=super().getDescription()
        woa_dic={'cross':'上下左右','longcross':'上下左右2格','circle':'附近8格','longcircle':'附近24格',
        'straight':'直线','queen':'直线与斜线','all':'全图'}
        s+='攻击方式：'+woa_dic[self.WOA]+'\n'
        return s   

class organ():
    def __init__(self,name,stats,endurance=10,existance=True):
        self.name=name
        self.stats=stats
        self.endurance=endurance
        self.existance=existance
    def check(self):
        if self.endurance<=0:
            self.existance=False
            self.stats={}

class player():
    def __init__(self,name,cookie):
        self.name=name
        self.cookie=cookie
        self.hp=100
        self.mp=50
        self.level=1
        self.exp=0
        self.tp=0
        self.sp=0
        self.bag={}
        #wears of a player
        self.wears={'左臂':None,
        '右臂':weapon('木棒',1,'cross',description='test'),
        '左腿':None,
        '右腿':None,
        '躯干':equipment('遮羞布',{'DEF':1},allow_list=['躯干'],description='你的初始装备，没有一点卵用'),
        '头':None,
        '内脏':None,
        '灵魂':None}
        #body parts of a player
        self.body={'左臂':organ('左臂',{'ATK':1}),
        '右臂':organ('右臂',{'ATK':1}),
        '左腿':organ('左腿',{'AGI':1}),
        '右腿':organ('右腿',{'AGI':1}),
        '躯干':organ('躯干',{'DEF':2,'MDE':2}),
        '头':organ('头',{'MAT':1,'ATK':1,'AGI':1}),
        '内脏':organ('内脏',{'MAT':1,'DEF':1,'MDE':1}),
        '灵魂':organ('灵魂',{'MAT':1,'LUK':3})}
        self.stats=initial_stats()
    
    def organ_stats(self,o):
        s={}
        if o in self.body:
            for i in ['ATK','DEF','MAT','MDE','AGI','LUK']:
                s[i]=self.body[o].stats.get(i,0)+self.wears[o].stats.get(i,0)
        return s

    def cal_stats(self,s):
        value=self.stats[s]
        for i in ['左臂','右臂','左腿','右腿','躯干','头','内脏','灵魂']:
            value+=self.body[i].stats.get(s,0)
            if self.wears[i]!=None:
                value+=self.wears[i].stats.get(s,0)
        return value

    def basic_info(self):
        s=''
        s+='姓名：'+self.name+'\n'
        s+='饼干：'+self.cookie+'\n'
        s+='HP：'+str(self.hp)+'\n'
        s+='MP：'+str(self.mp)+'\n'
        s+='等级：'+str(self.level)+'\n'
        for i in ['ATK','DEF','MAT','MDE','AGI','LUK']:
            s+=i+'：'+str(self.cal_stats(i))+'\n'
        return s
    
    def equipment_info(self):
        s=''
        part_name=['左臂','右臂','左腿','右腿','躯干','头','内脏','灵魂']
        for i in part_name:
            if self.body[i].existance:
                if self.wears[i]!=None:
                    s+=i+'装备了'+self.wears[i].name+'\n'
                s+=i+'的耐久：'+str(self.body[i].endurance)+'\n'
                for j in ['ATK','DEF','MAT','MDE','AGI','LUK']:
                    if j in self.body[i].stats:
                        s+=j+'：'+str(self.stats[j])+'\n'
            else:
                s+=i+'目前已损毁'+'\n'
        return s

    def check(self):
        part_name=['左臂','右臂','左腿','右腿','躯干','头','内脏','灵魂']
        for i in part_name:
            self.body[i].check()

    def level_info(self):
        s=''
        s+='等级：'+str(self.level)+'\n'
        s+='未用经验值：'+str(self.exp)+'\n'
        s+='未用能力点：'+str(self.tp)+'\n'
        s+='未用技能点：'+str(self.sp)+'\n'
        s+='当前等级所需经验：'+str((100+(self.level%10-1)*10)*2**(self.level//10))+'\n'
        return s

    def level_up(self):
        cost=(100+(self.level%10-1)*10)*2**(self.level//10)
        if self.exp>=cost:
            self.exp-=cost
            self.level+=1
            self.tp+=3
            self.sp+=1
            return True
        else:
            return False

    def add_tp(self,stat,point):
        if stat in self.stats:
            if point<=self.tp:
                self.tp-=point
                self.stats[stat]+=point
                return True
        else:
            return False

    def add_item(self,i,num):
        if i in self.bag:
            self.bag[i]+=num
        else:
            self.bag[i]=num
        return True

    def equip(self,i,loc):
        if i in self.bag:
            if isinstance(i,equipment) and loc in i.allow_list:
                self.add_item(self.wears[loc],1)
                self.wears[loc]=i
                self.bag[i]-=1
                return True
        return False



a=player('a','ABCDEFG')
print(a.basic_info())
# print(a.level_info())
# a.level=23
print(a.level_info())
print(a.equipment_info())
# print(type(a))
print(a.wears['躯干'].getDescription())
print(a.organ_stats('躯干'))

class block():
    def __init__(self,name,accessable,cate,hold=[]):
        self.name=name
        #whether a block can be reached
        self.accessable=accessable
        #category
        self.cate=cate
        #the characters(id) on this block
        self.hold=hold

class world_block(block):
    def __init__(self,name,accessable,hold=[]):
        block.__init__(self,name,accessable,hold,cate='big')

class map_block(block):
    def __init__(self,name,accessable,hold=[]):
        block.__init__(self,name,accessable,hold,cate='small')

class map_grid():
    def __init__(self,length,cate):
        self.length=length
        #grid contains block
        self.grid=[[None for i in range(length)] for j in range(length)]
        self.cate=cate
    def get_block(self,x,y):
        if x<self.length and y<self.length:
            return self.grid[y][x]
        return self.grid[0][0]