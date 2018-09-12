import sys
from pl0_lex import *
import collections

lexer = lex()
def generate_tokens(f):
    for tok in f:
        if not tok:
            pass
        else:
            yield tok

def gendo(x,y,z):
    cx = len(gentable)
    gentable.append([x,y,z])
    print(cx ,': ',x,y,z)

def set_gen(cx1,cx):
    i = gentable[cx1]
    i[2] = cx
    print('reset :',i,'from :',cx1)
    

class Parser(object):
    def parse(self,lex,lev,tx):
        self.lex = generate_tokens(lex)
        self.tok = None
        self.nexttok = None
        self._advance()
        return self.block(lev)# lev = 0  

    def _error(self,text = 'None'):
        print('ERROR :'+ text)

    def _advance(self):
        self.tok , self.nexttok = self.nexttok ,next(self.lex,None)
        print(self.tok)

    def _accept(self,toktype):
        if self.nexttok and self.nexttok.type == toktype:
            self._advance()
            return True
        else :
            return False
    def _expect(self,toktype):
        if not self._accept(toktype):
            raise SyntaxError ('Expected '+ toktype)
        else:
            return True
    def print_table(self,lev):
        print('\nstart table :')
        for i in table:
            print(i)
    def geti(self,name , lev):
        d = None
        for j in table:
            if j[0] == name and j[1] <= lev:
                d=j
        #print(d)
        return d
    
    def block(self, lev):
        dx0 = dx =3
        adr = 0
        tx0 = len(table)-1
        i = table[tx0]
        i[3] = len(gentable)
        gendo('jmp',0,0) #add 'ARRAY'
        while self._accept('CONST') or self._accept('VAR') or self._accept('PROCEDURE') or self._accept('ARRAY'):
            op1 = self.tok.type
            if op1 == 'CONST':
                self.accept_const(lev )
                while self._accept('COMMA') or self._accept('EOS'):
                    op2 = self.tok.type
                    if op2 == 'COMMA':
                        self.accept_const(lev)
                    else:
                        break
            elif op1 =='VAR':
                dx = self.accept_var(lev,dx)
                while self._accept('COMMA') or self._accept('EOS'):
                    op2 = self.tok.type
                    if op2 =='COMMA':
                        dx = self.accept_var(lev,dx)
                    else:
                        break
            elif op1 =='PROCEDURE':
                dx = self.accept_pro(lev,dx)
            else:#add
                dx = self.accept_array(lev,dx)
        set_gen(i[3],len(gentable))
        i = table[tx0]
        i[3] = len(gentable)
        i[4] = dx
        gendo('inte',0,dx )
        self.print_table(lev)
        self.statement(lev )
        gendo('opr',0,0 )

    def statement(self,lev):# 2018-1-9  9:21
        self._expect('BEGIN')
        while self._accept('ID') or self._accept('CALL')or self._accept('IF')or self._accept('FOR')or self._accept('READ')or self._accept('WHILE')or self._accept('WRITE'):
            op = self.tok.type
            if op =='ID':
                cx=self.set_var(lev )
            elif op =='CALL':
                cx=self.accept_call(lev )
            elif op =='IF':
                cx=self.accept_if(lev )
            elif op =='FOR':
                cx=self.accept_for(lev)
            elif op =='READ':
                cx=self.accept_read(lev)
            elif op =='WHILE':
                cx =self.accept_while(lev )
            elif op =='WRITE':
                cx =self.accept_write(lev )
        self._expect('END')
        if self._accept('EOS') or self._accept('DOT'):
            op = self.tok.type
            if op == 'DOT':
                return True

    def accept_write(self,lev):
        self._expect('LPAREN')
        self.expr(lev)
        gendo('opr',0,14)
        while self._accept('COMMA'):
            self.expr(lev)
            gendo('opr',0,14)
        self._expect('RPAREN')
        gendo('opr',0,15)
        self._expect('EOS')

    def accept_while(self,lev):  #59
        cx1 = len(gentable)
        self.accept_condition(lev)
        cx2 = len(gentable)
        gendo('jpc',0,0 )
        self._expect('DO')
        self.statement(lev)
        gendo('jmp',0,cx1)
        set_gen(cx2,len(gentable))

    def accept_read(self,lev): #55
        self._expect('LPAREN')
        if self._accept('ID'):
            name = self.tok.value
            i= self.geti(name,lev)
            if i != None:
                if i[2] == 'VAR':
                    gendo('opr',0,16)
                    gendo('sto',lev-i[1],i[4])
                elif i[2] == 'ARRAY':
                    self._expect('LZPAREN')
                    if self._accept('ID') or self._accept('NUMBER'):
                        op = self.tok.type
                        if op == 'NUMBER':
                            num = self.tok.value
                            if num <= len(i[3]):
                                adr = i[4]
                                gendo('opr',0,16)
                                gendo('sto',lev-i[1],i[5]+num)
                            else:
                                self._error()
                        else:
                            NumName = self.tok.value
                            Numi = self.geti(NumName,lev)
                            if Numi[2]=='CONST':
                                num = Numi[3]
                                if num in i[3]:
                                    adr = i[4]
                                    gendo('opr',0,16)
                                    gendo('sto',lev-i[1],i[5]+num)
                                else:
                                    self._error()
                            else:
                                self._error()
                    self._expect('RZPAREN')
                else:
                    self._error('error')
            else:
                self._error('error')
        else:
            self._error('error')
        while self._accept('COMMA'):
            if self._accept('ID'):
                name = self.tok.value
                i=self.geti(name,lev)
                if i != None:
                    if i[2] == 'VAR':
                        gendo('opr',0,16)
                        gendo('sto',lev-i[1],i[4])
                    else:
                        self._error('error')
                else:
                    self._error('error')
            else:
                self._error('error')
        self._expect('RPAREN')
        self._expect('EOS')

    def accept_for(self,lev):
        self.statement(lev)

    def accept_if(self,lev ):
        self.accept_condition(lev)
        if self._accept('THEN'):
            cx1 = len(gentable)
            gendo('jpc',0,0 )
            self.statement(lev)
            set_gen(cx1,len(gentable))
            if self._accept('ELSE'):
                self.statement(lev)
        else:
            self._error()
    
    def accept_call(self,lev ):# P40
        if self._accept('ID'):
            name = self.tok.value
            i = self.geti(name,lev)
            if i == None :
                self._error('1')
            elif i[2] == 'PRO':
                gendo('cal',lev-i[1],i[3])
            else:
                self._error('2')
        self._expect('EOS')

    def set_var(self,lev):
        name = self.tok.value
        i = self.geti(name,lev)#name 和当前层
        if i == None:
            self._error('the name is not in table ! --> '+name)
        elif i[2] is not 'VAR':
            self._error('the name is not a VAR ! --> '+name)
        elif self._accept('EQ') or self._accept('DPLUS') or self._accept('DMINUS'):
            op = self.tok.type
            if op == 'EQ':
                self.expr(lev)
                gendo('sto',lev-i[1],i[4] )
            elif op == 'DPLUS':
                gendo('lod',lev-i[1],i[4])
                gendo('lit',0,1)
                gendo('opr',0,2)
                gendo('sto',lev-i[1],i[4])
            elif op == 'DMINUS':
                gendo('lod',lev-i[1],i[4])
                gendo('lit',0,1)
                gendo('opr',0,3)
                gendo('sto',lev-i[1],i[4])
            self._expect('EOS')
        else:
            self._error()


    def accept_array(self,lev ,dx): #add
        if self._accept('ID'):
            name = self.tok.value
            self._expect('LZPAREN')
            if self._accept('NUMBER') or self._accept('ID'):
                op = self.tok.type
                if op == 'NUMBER':
                    num = self.tok.value
                    table.append([name,lev,'ARRAY',[None]*num,[range(dx,dx+num)],dx])
                    dx+=num
                else:
                    cname = self.tok.value
                    i = self.geti(cname,lev)
                    if i[2] == 'CONST':
                        table.append([name,lev,'ARRAY',[None]*i[3],[range(dx,dx+i[3])],dx])
                        dx+=i[3]
                    else:
                        self._error()
            self._expect('RZPAREN')
            self._expect('EOS')
            return dx
    
    def accept_const(self,lev):
        if self._accept('ID'):
            name = self.tok.value
            if self._accept('CEQ'):
                if self._accept('NUMBER'):
                    table.append([name,lev,'CONST',self.tok.value])
                else:
                    self._error()
            else:
                self._error('not "=" in const ! -->'+ name)

    def accept_var(self,lev,dx):
        if self._accept('ID'):
            name = self.tok.value
            table.append([name,lev,'VAR',None,dx])
            return dx+1

    def accept_pro(self,lev,dx):
        if self._accept('ID'):
            name = self.tok.value
            table.append([name,lev,'PRO',dx,0])
            if not self._accept('EOS'):
                self._error('Result not the ";" ')
            else :
                self.block(lev+1)
        return dx
                    
    def accept_condition(self,lev):
        if self._accept('ID') or self._accept('NUMBER') or self._accept('ODD'):
            op =self.tok.type
            if op =='ODD':
                self.expr(lev)
                gendo('opr',0,6)
            else:
                self.expr(lev)
                if self._accept('GE') or self._accept('LE') or self._accept('GT') or self._accept('LT') or self._accept('NEQ') or self._accept('EQEQ'):
                    op = self.tok.type
                    self.expr(lev)
                    if op =='EQEQ':
                        gendo('opr',0,8 )
                    elif op == 'NEQ':
                        gendo('opr',0,9 )
                    elif op == 'LT':
                        gendo('opr',0,10)
                    elif op == 'GE':
                        gendo('opr',0,11 )
                    elif op == 'GT':
                        gendo('opr',0,12 )
                    else:
                        gendo('opr',0,13)
                else:
                    self._error()
        else:
            self._error()

    def expr(self,lev):
        ''' '''
        if self._accept('PLUS') or self._accept('MINUS') :
            op = self.tok.type
            self.term(lev)
            if op =='PLUS':
                pass
            elif op =='MINUS':
                gendo('opr',0,1)
        else:
            self.term(lev)
        while self._accept('PLUS') or self._accept('MINUS'):
            op = self.tok.type
            self.term(lev)
            if op == 'PLUS':
                gendo('opr',0,2)
            else:
                gendo('opr',0,3)

    def term(self,lev):
        '''  '''
        self.factor(lev)
        while self._accept('TIMES') or self._accept('DIVIDE'):
            op = self.tok.type
            self.factor(lev)
            if op == 'TIMES':
                gendo('opr',0,4)
            elif op =='DIVIDE':
                gendo('opr',0,5)

    def factor(self,lev):
        ''' '''
        while self._accept('NUMBER') or self._accept('LPAREN') or self._accept('ID'):
            op = self.tok.type
            if op == 'NUMBER':
                gendo('lit',0,self.tok.value)
            elif op =='LPAREN':
                self.expr(lev)
                self._accept('RPAREN')
            else:
                name = self.tok.value
                i = self.geti(name,lev)
                if i[2] == 'VAR':
                    gendo('lod',lev-i[1],i[4])
                elif i[2] == 'CONST':
                    gendo('lit',0,i[3])
                else:
                    self._error()
        
if __name__ == '__main__':
    filename = input('please input the filename : ')
    f = open(filename).read()
    lexer.input(f)
    gentable =[]
    table = [['None',0,'Pro',0,0]]
    e = Parser()
    e.parse(lexer,0,0)
    #'''
    print('start PL0:')
    x=0
    for i in gentable :
        print(x, ':',i[0],i[1],i[2])
        x+=1
    #'''
            
