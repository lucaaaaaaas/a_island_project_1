from random import *

global player_dic
player_dic={}
global item_dic
item_dic={}
global skill_dic
skill_dic={}
global block_dic
block_dic={}

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

class buff_item(item):
    def __init__(self,name,purpose,description='',usage=1):
        item.__init__(self,name,description=description, usage=usage)
        self.purpose=purpose

class equipment(item):
    def __init__(self,name,stats,allow_list=[],ability={},description=''):
        item.__init__(self,name,description=description,usage=-1)
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

test_medicine=buff_item('超级伤药',{'HP':100,'MP':100,'ATK':5})
item_dic['超级伤药']=test_medicine
medicine00=buff_item('小红瓶',{'HP':50})
item_dic['小红瓶']=medicine00
medicine01=buff_item('红瓶',{'HP':100})
item_dic['红瓶']=medicine01
medicine02=buff_item('大红瓶',{'HP':200})
item_dic['大红瓶']=medicine02
medicine03=buff_item('超红瓶',{'HP':400})
item_dic['超红瓶']=medicine03
medicine04=buff_item('喝不下的红瓶',{'HP':9999})
item_dic['喝不下的红瓶']=medicine04
medicine05=buff_item('小蓝瓶',{'MP':25})
item_dic['小蓝瓶']=medicine05
medicine06=buff_item('蓝瓶',{'MP':50})
item_dic['蓝瓶']=medicine06
medicine07=buff_item('大蓝瓶',{'MP':100})
item_dic['大蓝瓶']=medicine07
medicine08=buff_item('超蓝瓶',{'MP':200})
item_dic['超蓝瓶']=medicine08
medicine09=buff_item('喝到吐的蓝瓶',{'MP':9999})
item_dic['喝到吐的蓝瓶']=medicine09
medicine10=buff_item('小紫瓶',{'HP':50,'MP':50})
item_dic['小紫瓶']=medicine10
medicine11=buff_item('紫瓶',{'HP':100,'MP':100})
item_dic['紫瓶']=medicine11
medicine12=buff_item('大紫瓶',{'HP':200,'MP':200})
item_dic['大紫瓶']=medicine12
medicine13=buff_item('超紫瓶',{'HP':400,'MP':400})
item_dic['超紫瓶']=medicine13
medicine14=buff_item('色素怼太多的紫瓶',{'HP':9999,'MP':9999})
item_dic['色素怼太多的紫瓶']=medicine14
medicine15=buff_item('祝福：力之金阁',{'ATK':2})
item_dic['祝福：力之金阁']=medicine15
medicine16=buff_item('祝福：技之银阁',{'MAT':2})
item_dic['祝福：技之银阁']=medicine16
medicine17=buff_item('祝福：动之铜阁',{'AGI':2})
item_dic['祝福：动之铜阁']=medicine17
medicine18=buff_item('祝福：守之铁阁',{'DEF':2})
item_dic['祝福：守之铁阁']=medicine18
medicine19=buff_item('祝福：深邃幻想',{'MDE':2})
item_dic['祝福：深邃幻想']=medicine19
medicine20=buff_item('祝福：自由热舞',{'LUK':2})
item_dic['祝福：自由热舞']=medicine20
medicine21=buff_item('祝福：王者祝福',{'ATK':2,'DEF':2,'MAT':2,'MDE':2,'AGI':2,'LUK':2})
item_dic['祝福：王者祝福']=medicine21

class organ():
    def __init__(self,name,part,stats,endurance=10,existance=True):
        self.name=name
        self.part=part
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
        self.body={'左臂':organ('左臂','左臂',{'ATK':0.1,'HP':0.5}),
        '右臂':organ('右臂','右臂',{'ATK':0.1,'HP':0.5}),
        '左腿':organ('左腿','左腿',{'AGI':0.1,'HP':0.5}),
        '右腿':organ('右腿','右腿',{'AGI':0.1,'HP':0.5}),
        '躯干':organ('躯干','躯干',{'DEF':0.2,'MDE':0.2,'HP':3}),
        '头':organ('头','头',{'MAT':0.1,'ATK':0.1,'AGI':0.1,'HP':2,'MP':1.5}),
        '内脏':organ('内脏','内脏',{'MAT':0.1,'DEF':0.1,'HP':2,'MDE':0.1}),
        '灵魂':organ('灵魂','灵魂',{'MAT':0.1,'LUK':0.3,'MP':2.5})}
        self.stats=initial_stats()
        self.stats['HP']=10
        self.stats['MP']=10
        #position of a player
        self.map_pos=[0,0]
        #position of a player on a certain map
        self.world_pos=[0,0]
        self.is_dead=False
        self.skills=[]

    def cal_stats(self,s):
        value=self.stats[s]
        for i in ['左臂','右臂','左腿','右腿','躯干','头','内脏','灵魂']:
            value+=self.body[i].stats.get(s,0)*self.body[i].endurance
            if self.wears[i]!=None:
                value+=self.wears[i].stats.get(s,0)
        return value

    def basic_info(self):
        s=''
        s+='姓名：'+self.name+'\n'
        s+='饼干：'+self.cookie+'\n'
        s+='等级：'+str(self.level)+'\n'
        for i in self.stats.keys():
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
        # if self.hp>self.maxhp:
        #     self.hp=self.maxhp
        # if self.mp>self.maxmp:
        #     self.mp=self.maxmp
        if self.stats['HP']<=0:
            self.is_dead=True

    def level_info(self):
        s=''
        s+='等级：'+str(self.level)+'\n'
        s+='未用经验值：'+str(self.exp)+'\n'
        s+='未用能力点：'+str(self.tp)+'\n'
        s+='未用技能点：'+str(self.sp)+'\n'
        s+='当前等级所需经验：'+str((100+(self.level%10-1)*10)*2**(self.level//10))+'\n'
        return s

    def bag_info(self):
        s=''
        for key in self.bag.keys():
            if self.bag[key]>0:
                s+='名称：'+key+'\n可用次数：'+str(self.bag[key])+'\n'
        if s=='':
            s='你没有任何物品'
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

    def add_item(self,i):
        global item_dic
        if i in item_dic.keys():
            if i in self.bag.keys():
                self.bag[i]+=item_dic[i].usage
            else:
                self.bag[i]=item_dic[i].usage
            return True
        else:
            return False

    def equip(self,i,loc):
        if i in self.bag:
            if isinstance(i,equipment) and loc in i.allow_list:
                self.add_item(self.wears[loc],1)
                self.wears[loc]=i
                self.bag[i]-=1
                return True
        return False

    def use(self,name):
        global item_dic
        if name in self.bag.keys() and name in item_dic.keys():
            thing=item_dic[name]
            if self.bag[name]>0:
                for key in thing.purpose.keys():
                    if key in self.stats.keys():
                        self.stats[key]+=thing.purpose[key]
                self.bag[name]-=1
                if self.bag[name]==0:
                    del self.bag[name]
                return True
        else:
            return False

    def apply(self,sk,to=None):
        global player_dic
        global skill_dic
        if sk in self.skills:
            if sk in skill_dic:
                if to==None or to in player_dic:
                    #should be a function
                    if skill_dic[sk](self,to):
                        if to in player_dic:
                            to.check()
                        return '成功'
                    return '无效的操作'
                return '无效的对象'
            return '此技能不存在'
        return '你并不拥有此技能'

def create_player(name,cookie):
    global player_dic
    a=player(name,cookie)
    player_dic[cookie]=a

def damage(a,b):
    b.stats['HP']-=100
    return True

def hurt(a,b):
    for i in b.body:
        i.endurance-=1
    return True


create_player('a','ABCDEFG')
a=player_dic['ABCDEFG']
print(a.basic_info())
a.add_item('超级伤药')
a.add_item('超级伤药')
print(a.bag_info())
a.use('超级伤药')
print(a.basic_info())
print(a.bag_info())
# # print(a.level_info())
# # a.level=23
# print(a.level_info())
# print(a.equipment_info())
# # print(type(a))
# print(a.wears['躯干'].getDescription())
# print(a.organ_stats('躯干'))

class block():
    def __init__(self,name,cate,accessable=True,hold=[]):
        self.name=name
        #whether a block can be reached
        self.accessable=accessable
        #category
        self.cate=cate
        #the characters(id) on this block
        self.hold=hold

class world_block(block):
    def __init__(self,name,accessable=True,hold=[]):
        block.__init__(self,name,'big',accessable=accessable,hold=hold)

class map_block(block):
    def __init__(self,name,accessable=True,hold=[]):
        block.__init__(self,name,'small',accessable=accessable,hold=hold)

class grid():
    def __init__(self,length,cate):
        self.length=length
        #grid contains block
        self.grid=[[None for i in range(length)] for j in range(length)]
        self.cate=cate
    def get_block(self,x,y):
        if x<self.length and y<self.length:
            return self.grid[y][x]
        return False

class map_grid(grid):
    def __init__(self,length):
        map_grid.__init__(self,length,cate='small')
    def mov(self,character,x,y):
        if self.get_block(x,y).accessable:
            self.get_block(character.map_pos[0],character.map_pos[1]).hold.remove(character)
            character.pos=[x,y]
            self.get_block(x,y).hold+=character
            return True
        else:
            return False

class world_grid(grid):
    def __init__(self,length):
        map_grid.__init__(self,length,cate='big')
    def mov(self,character,x,y):
        if self.get_block(x,y).accessable:
            self.get_block(character.world_pos[0],character.world_pos[1]).hold.remove(character)
            character.world_pos=[x,y]
            self.get_block(x,y).hold+=character
            return True
        else:
            return False
