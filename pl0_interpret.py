from pl0_parser import *

def get_parser(p):
    for i in p:
        if not i:
            pass
        else:
            yield i

class Interpret(object):
    def interpret(self,parser,f):
        self.parser = get_parser(parser)
        self.line = None
        self._accept()
        return self._main(f)
        
    def _advance(self):
        self.line = next(self.parser,None)
        print(self.line)

    def _main(self,f):
        p=b=t=0
        i=0
        s = [None]*500
        print('start pl0',file = inf)
        s[0] = s[1] = s[2] =0
        while _accept():
            i = self.line
            if i[0] == 'lit':
                s[t] = int(i[2])
                t+=1
            elif i[0] == 'opr':
                a = int(i[2])
                if a==0:
                    t=b
                    p=s[t+2]
                    b=s[t+1]
                elif a==1:
                    s[t-1] = -s[t-1]
                elif a==2:
                    t-=1
                    s[t-1] = s[t-1]+s[t]
                elif a==3:
                    t-=1
                    s[t-1] = s[t-1]-s[t]
                elif a==4:
                    t-=1
                    s[t-1] = s[t-1]*s[t]
                elif a==5:
                    t-=1
                    s[t-1] = s[t-1]/s[t]
                elif a==6:
                    t-=1
                    s[t-1] = s[t-1]%2
                elif a==8:
                    t-=1
                    s[t-1] = (s[t-1] == s[t])
                elif a==9:
                    t-=1
                    s[t-1] = (s[t-1] != s[t])
                elif a==10:
                    t-=1
                    s[t-1] = (s[t-1] < s[t])
                elif a==11:
                    t-=1
                    s[t-1] = (s[t-1] >= s[t])
                elif a==12:
                    t-=1
                    s[t-1] = (s[t-1] > s[t])
                elif a==13:
                    t-=1
                    s[t-1] = (s[t-1] <= s[t])
                elif a==14:
                    print(s[t-1])
                    print(s[t-1] ,file = f)
                    t-=1
                elif a==15:
                    print('\n')
                    print('\n' ,file = f)
                elif a==16:
                    num = input('? :')
                    print('? : ',num,file = f)
                    t+=1
            elif i[0] =='lod':
                point = self.base(i[1],b)+i[0]
                s[t] = s[point]
                t+=1
            elif i[0] == 'sto':
                t-=1
                point = self.base(i[1],b)+i[0]
                s[point] = s[t]
            elif i[0] == 'cal':
                s[t] = self.base(i[1],b)
                s[t+1] = b
                s[t+1] = p
                b=t
                p = i[0]
            elif i[0] == 'init':
                t+=i[0]
            elif i[0] == 'jmp':
                p=i[0]
            elif i[0]=='jpc':
                t-=1
                if s[t]==0:
                    p = i[0]

    def base(self,l,b):
        t = b
        while l>0:
            b1 = s[b1]
            l-=1
        return b1

if __name__ =='__main__':
    filename = input('please input the filename : ')
    f = open(filename).read()
    save = open('pl0_table','wt')
    lexer.input(f)
    gentable =[]
    table = [['None',0,'Pro',0,0]]
    e = Parser()
    e.parse(lexer,0,0)
    e.print_table()
    end = Interpret()
    end.interpret(e,save)
