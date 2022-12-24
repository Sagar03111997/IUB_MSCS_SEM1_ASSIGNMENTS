class Wavelet_Tree :
    def __init__(self , array) :

        self.dict = []
        queue = []
        queue.append(array)
        while queue:
            arr = queue.pop(0)
            if arr[0] == ['1']:
                if arr[1] == ['X']:
                    self.dict.append('X')
                    self.dict.append(arr[2])
                else:
                    self.dict.append(arr[1])
                    self.dict.append('X')
                continue

            elif arr == ['2']:
                self.dict.append('X')
                self.dict.append('X')
                continue

            else:
                array_str = ""
                mid = sum(arr) // len(arr) + 1
                for n in arr:
                    if n >= mid:
                        array_str += "1"
                    else:
                        array_str += "0"

                l = [n for n in arr if n < mid]
                r = [n for n in arr if n >= mid]

                if len(l) <= 1 and len(r) <= 1:
                    self.dict.append(array_str)
                    queue.append(['2'])
                    continue

                elif len(l) <= 1 or len(r) <= 1:
                    self.dict.append(array_str)

                    if len(l) <= 1:
                        array_str = []
                        array_str.append(['1'])
                        array_str.append(['X'])
                        mid = sum(r) // len(r) + 1

                        result = ""
                        for n in r:
                            if n >= mid:
                                result += "1"
                            else:
                                result += "0"
                        array_str.append(result)
                        queue.append(array_str)    
                        continue

                    else:    
                        array_str = []
                        array_str.append(['1'])
                        mid = sum(l)//len(l)+1
                        result = ""

                        for n in l:
                            if n >= mid:
                                result += "1"
                            else:
                                result += "0"

                        array_str.append(result)
                        array_str.append(['X'])
                        queue.append(array_str)       
                        continue

                self.dict.append(array_str)
                queue.append(l)
                queue.append(r)        
    

    def RQQ(self , k : int , left : int , right : int):
        print(f'Level {0} :',(k, left, right))

        if left >= right:
            return
        c = self.dict[0][left - 1: right].count('0')

        if c < k:
            l = self.dict[0][:left - 1].count('1') + 1
            r = self.dict[0][:right].count('1')
            self.RQQ_helper(2 * 0+2, k-c, l, r, 0+1)

        else:
            l = self.dict[0][:left-1].count('0')+1
            r = self.dict[0][:right].count('0')
            self.RQQ_helper(2 * 0+1 , k, l, r, 0+1)
        return

    def print(self) :
        i = 0
        l = 0
        while(i < len(self.dict)):
            print(f'Level {l} : ', end = "")

            for j in range(i, min(len(self.dict), 2**l+i)):
                if j == min(len(self.dict), 2**l+i) - 1:
                    print(self.dict[j])
                else:
                    print(self.dict[j],', ', end = "")
            l += 1
            i = 2 ** (l) - 1
        return

wv = Wavelet_Tree([6, 2, 0, 7, 9, 3, 1, 8, 5, 4])
wv.print()

