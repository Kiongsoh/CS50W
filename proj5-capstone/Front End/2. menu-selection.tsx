import { useState } from 'react'
import { ChevronLeft, Clock, MapPin, Star } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

export default function MenuSelection() {
  const [activeTab, setActiveTab] = useState("today's-offer")

  const restaurantInfo = {
    name: "CHAGEE - Plaza Singapura",
    category: "Coffee & Tea",
    rating: 4.6,
    time: "45 mins",
    distance: "2.2 km",
    openingHours: "Today 10:00-21:30",
    promos: [
      "S$3.00 off delivery fee with S$26.00 min. order",
      "Enjoy discounts on items",
    ],
  }

  const menuCategories = [
    "Today's Offer",
    "Fresh Milk Tea Series",
    "Teaspresso • Tea Latte",
    "Brewed Tea Series",
    "Iced Oriental Tea Series",
    "Bakery",
  ]

  const menuItems = [
    {
      name: "Lapsang Souchong Tea Latte(Regular)",
      price: 5.44,
      originalPrice: 6.40,
      image: "/placeholder.svg?height=100&width=100",
    },
    // Add more menu items here
  ]

  return (
    <div className="container mx-auto p-4">
      <header className="flex items-center gap-4 mb-6">
        <Button variant="ghost" size="icon">
          <ChevronLeft className="h-6 w-6" />
        </Button>
        <h1 className="text-2xl font-bold">{restaurantInfo.name}</h1>
      </header>

      <Card className="mb-6">
        <CardContent className="p-4">
          <p className="text-gray-600 mb-2">{restaurantInfo.category}</p>
          <div className="flex items-center gap-4 text-sm mb-2">
            <span className="flex items-center"><Star className="h-4 w-4 mr-1" /> {restaurantInfo.rating}</span>
            <span className="flex items-center"><Clock className="h-4 w-4 mr-1" /> {restaurantInfo.time}</span>
            <span className="flex items-center"><MapPin className="h-4 w-4 mr-1" /> {restaurantInfo.distance}</span>
          </div>
          <p className="text-sm mb-2">Opening Hours: {restaurantInfo.openingHours}</p>
          {restaurantInfo.promos.map((promo, index) => (
            <p key={index} className="text-sm text-green-600">{promo}</p>
          ))}
        </CardContent>
      </Card>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="mb-6">
        <TabsList className="w-full overflow-x-auto">
          {menuCategories.map((category) => (
            <TabsTrigger key={category} value={category.toLowerCase().replace(' ', '-')}>
              {category}
            </TabsTrigger>
          ))}
        </TabsList>
      </Tabs>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {menuItems.map((item, index) => (
          <Card key={index}>
            <CardContent className="p-4 flex">
              <img src={item.image} alt={item.name} className="w-24 h-24 object-cover rounded-md mr-4" />
              <div>
                <CardTitle className="text-lg mb-2">{item.name}</CardTitle>
                <p className="text-lg font-bold">${item.price.toFixed(2)}</p>
                {item.originalPrice && (
                  <p className="text-sm text-gray-500 line-through">${item.originalPrice.toFixed(2)}</p>
                )}
                <Button className="mt-2">Add to Order</Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}