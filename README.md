# albionprofits
There is an API for developers to get it in json format instead of a graphical interface.  

At the moment there is only one point for obtaining profitable deals between the two cities.

***Good deals between two cities (JSON)***
                
https://albionprofits.ru/api/albion/prices/cities?format=json&locations=Black%20Market,Martlock&category_items=mellee_sword&tier=T4,T5,T6,T7,T8&chart=0,@1,@2,@3&profit=&hours=

---
  *Params:*
* locations:  in turn, the city of purchase, the city of sale - For the black market there is an exception, it must be specified first.
* category_items: category of items to search. More details below.
* tiers: tier of items.
* chart: enchant for items.
* profit: Expected profit for one sale.
* hours: Information relevance.

 *Item Category:*
 * mellee_sword: Swords
 * range: Ranged weapon
 * mellee_mace
 * mellee_staff
 * mellee_hammer
 * mellee_daggers
 * mellee_axe
 * staff: Staves/Magic
 * plate_shoes
 * plate_head
 * plate_armor
 * leather_shoes
 * leather_head
 * leather_armor
 * cloth_shoes
 * cloth_armor
 * cloth_head
 * capes
 * bags
 * luxury
 * resources
