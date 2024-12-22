import { useState } from 'react'
import { Search, ShoppingBag } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export default function RestaurantSelection() {
  const [searchQuery, setSearchQuery] = useState('')

  const promotions = [
    { title: 'Only with Grab', image: '/placeholder.svg?height=100&width=200' },
    { title: 'Unlimited Savings', image: '/placeholder.svg?height=100&width=200' },
    { title: "McDonald's 1-for-1", image: '/placeholder.svg?height=100&width=200' },
    { title: '5-Star Eats', image: '/placeholder.svg?height=100&width=200' },
    { title: 'Up to 20% Off!', image: '/placeholder.svg?height=100&width=200' },
    { title: 'Islandwide Delivery', image: '/placeholder.svg?height=100&width=200' },
  ]

  const restaurants = [
    { name: 'CHAGEE - Plaza Singapura', cuisine: 'Coffee & Tea', rating: 4.6, time: '45 mins', distance: '2.2 km', promo: 'Free Delivery (Min. spend S$30)' },
    { name: 'CHICHA San Chen - CIMB Plaza', cuisine: 'Drinks & Beverages, Coffee & Tea, Bubble Tea', rating: 4.4, time: '30 mins', distance: '1.6 km', promo: 'Free Delivery (Min. spend S$35)' },
    { name: "McDonald's - City Square Mall", cuisine: 'Burger, Fast Food, Halal', rating: 4.4, time: '35 mins', distance: '3.7 km', promo: 'Free Delivery (Min. spend S$25)' },
    { name: 'KOI Thé - One Raffles Place', cuisine: 'Bubble Tea, Coffee & Tea, Drinks & Beverages', rating: 4.4, time: '30 mins', distance: '1.4 km', promo: '' },
  ]

  return (
    <div className="container mx-auto p-4">
      <header className="flex justify-between items-center mb-6">
        <img src="/placeholder.svg?height=40&width=120" alt="GrabFood" className="h-10" />
        <div className="flex items-center gap-4">
          <Button variant="outline" size="icon">
            <ShoppingBag className="h-4 w-4" />
          </Button>
          <Button variant="outline">Login/Sign Up</Button>
        </div>
      </header>

      <div className="relative mb-6">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
        <Input
          type="text"
          placeholder="Search for a dish or a restaurant"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="pl-10 pr-4 py-2 w-full"
        />
      </div>

      <div className="mb-8">
        <div className="flex gap-4 overflow-x-auto pb-4">
          {promotions.map((promo, index) => (
            <Card key={index} className="flex-shrink-0 w-48">
              <CardContent className="p-2">
                <img src={promo.image} alt={promo.title} className="w-full h-24 object-cover rounded-md" />
                <p className="text-sm mt-2 text-center">{promo.title}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      <h2 className="text-2xl font-bold mb-4">Popular Restaurants Near You</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {restaurants.map((restaurant, index) => (
          <Card key={index}>
            <CardContent className="p-4">
              <img src="/placeholder.svg?height=150&width=300" alt={restaurant.name} className="w-full h-40 object-cover rounded-md mb-4" />
              <CardTitle className="text-lg mb-2">{restaurant.name}</CardTitle>
              <p className="text-sm text-gray-600 mb-2">{restaurant.cuisine}</p>
              <div className="flex items-center gap-2 text-sm">
                <span>⭐ {restaurant.rating}</span>
                <span>🕒 {restaurant.time}</span>
                <span>📍 {restaurant.distance}</span>
              </div>
              {restaurant.promo && (
                <p className="text-sm text-green-600 mt-2">{restaurant.promo}</p>
              )}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}