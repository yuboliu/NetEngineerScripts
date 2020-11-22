#!/usr/bin/tclsh

puts "Hello World"

set myVariable 18
puts [expr $myVariable + 6 + 9]
puts "---动态类型语言"

set a 3
set variableA test
set {variable B} test
puts $variableA
puts ${variable B}
puts "---变量赋值的3种方式"

set a 10;
set b [expr $a == 1 ? 20: 30]
puts "Value of b is $b"
set b [expr $a == 10 ? 20: 30]
puts "Value of b is $b"
puts "---三元运算符?: 用法"

set myVariable {red green blue}
puts [lindex $myVariable 2]
set myVariable "red green blue"
puts [lindex $myVariable 1]
puts "---List 使用"

set  marks(english) 80
puts $marks(english)
set  marks(mathematics) 90
puts $marks(mathematics)
puts "---数组使用"

set a 10
if { $a < 20  } {
    puts "a is less than 20"
}
puts "value of a is : $a"
puts "---if 语句"

set a 100
if { $a == 10 } {
   puts "Value of a is 10"
} elseif { $a == 20 } {
   puts "Value of a is 20"
} elseif { $a == 30 } {
   puts "Value of a is 30"
} else {
   puts "None of the values is matching"
}
puts "Exact value of a is: $a"
puts "---if...elseif..else 语句"

set grade C;
switch $grade --A { puts "Well done!" }  B { puts "Excellent!" }  C { puts "You passed!"  } F { puts "Better try again"   }   default {     puts "Invalid grade"   }
puts "Your grade is  $grade"
puts "---switch 语句一行写法"

set grade B;
switch --$grade {
   A {
      puts "Well done!"
   }
   B {
      puts "Excellent!"
   }
   C {
      puts "You passed!"
   }
   F {
      puts "Better try again"
   }
   default {
      puts "Invalid grade"
   }
}
puts "Your grade is  $grade\n"
puts "---switch 语句多行写法"

set a 19
while { $a < 20 } {
   puts "value of a: $a"
   incr a
}
puts "while\n"
puts "---while 循环"

for { set a 18}  {$a < 20} {incr a} {
   puts "value of a: $a"
}
puts "for\n"
puts "---for 循环"

set a 14
while {$a < 17 } {
   puts "value of a: $a"
   incr a
   if { $a > 15} {
          break
   }
}
puts "break\n"
puts "---break"

set a 14
while { $a < 17 } {
   if { $a == 15} {
       incr a
       continue
   }
   puts "value of a: $a"
   incr a
}
puts "continue\n"
puts "---continue"

set languages(0) Tcl
set languages(1) "C Language"
puts $languages(0)
puts $languages(1)
puts "---数组"

puts [array size languages]
puts "---计算数组大小的语法"

set languages(0) Tcl
set languages(1) "C Language"
for { set index 0  }  { $index < [array size languages]  }  { incr index  } {
    puts "languages($index) : $languages($index)"
}
puts "---数组迭代"

set personA(Name) "Dave"
set personA(Age) 14
puts [array names personA]
puts "---获取数组索引"

set personA(Name) "Dave"
set personA(Age) 14
foreach index [array names personA] {
    puts "personA($index): $personA($index)"
}
puts "---使用数组的索引来遍历数组"

set colorList1 {red green blue}
set colorList2 [list red green blue]
set colorList3 [split "red_green_blue" _]
puts $colorList1
puts $colorList2
puts $colorList3
puts "---定义List"

set var {orange blue red green}
puts [lindex $var 1]
puts "---列表索引"

puts "\n"
dict set colours colour1 red
puts $colours
dict set colours colour2 green
puts $colours

set colours [dict create colour1 "black" colour2 "white"]
puts $colours
puts "---创建字典"

set colours [dict create colour1 "black" colour2 "white"]
set value [dict get $colours colour1]
puts $value
puts "---获取字典中指定Key对应的Value"

set colours [dict create colour1 "black" colour2 "white"]
set keys [dict keys $colours]
puts $keys
puts "---获取字典中的key"

set colours [dict create colour1 "black" colour2 "white"]
set values [dict values $colours]
puts $values
puts "---获取字典中的value"

set colours [dict create colour1 "black" colour2 "white"]
foreach item [dict keys $colours] {
    set value [dict get $colours $item]
    puts $value
}
puts "---遍历字典，获取所有的Value"

set colours [dict create colour1 "black" colour2 "white"]
puts [dict exists $colours colour1]
puts "---判断字典中是否存在该Key"

proc helloWorld {} {
    puts "Hello, World!"
}
helloWorld
puts "---无参数函数"

proc add {a b} {
    return [expr $a+$b]
}
puts [add 10 30]
puts "---函数带参数"

proc avg {numbers} {
    set sum 0
    foreach number $numbers {
      set sum  [expr $sum + $number]
	}
    set average [expr $sum/[llength $numbers]]
    return $average
}
puts [avg {70 80 50 60}]
puts [avg {70 80 50 }]
puts "---函数可变参数"

proc add {a {b 100} } {
   return [expr $a+$b]
}
puts [add 10 30]
puts [add 10]
puts "---函数默认参数"

namespace eval MyMath {
  variable myResult
}
proc MyMath::Add {a b } {
  set ::MyMath::myResult [expr $a + $b]
}
MyMath::Add 10 23
puts $::MyMath::myResult
puts "---创建命令空间"


