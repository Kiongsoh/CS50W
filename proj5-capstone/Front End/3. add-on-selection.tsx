import { useState } from 'react'
import { X } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"

export default function AddOnSelection() {
  const [sweetness, setSweetness] = useState('normal')
  const [iceLevel, setIceLevel] = useState('normal')
  const [specialInstructions, setSpecialInstructions] = useState('')

  const item = {
    name: "Lapsang Souchong Tea Latte(Regular)",
    price: 5.44,
    originalPrice: 6.40,
    image: "/placeholder.svg?height=100&width=100",
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="flex justify-between items-center">
          <CardTitle>{item.name}</CardTitle>
          <Button variant="ghost" size="icon">
            <X className="h-6 w-6" />
          </Button>
        </CardHeader>
        <CardContent>
          <div className="flex items-center mb-4">
            <img src={item.image} alt={item.name} className="w-16 h-16 object-cover rounded-md mr-4" />
            <div>
              <p className="text-lg font-bold">${item.price.toFixed(2)}</p>
              {item.originalPrice && (
                <p className="text-sm text-gray-500 line-through">${item.originalPrice.toFixed(2)}</p>
              )}
            </div>
          </div>

          <div className="mb-4">
            <h3 className="text-lg font-semibold mb-2">Sweetness Level</h3>
            <RadioGroup value={sweetness} onValueChange={setSweetness}>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="normal" id="normal-sweet" />
                <Label htmlFor="normal-sweet">Normal Sweet</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="no-sugar" id="no-sugar" />
                <Label htmlFor="no-sugar">No Additional Sugar</Label>
              </div>
            </RadioGroup>
          </div>

          <div className="mb-4">
            <h3 className="text-lg font-semibold mb-2">Ice Level</h3>
            <RadioGroup value={iceLevel} onValueChange={setIceLevel}>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="normal" id="normal-ice" />
                <Label htmlFor="normal-ice">Normal Ice</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="hot" id="hot" />
                <Label htmlFor="hot">Hot</Label>
              </div>
            </RadioGroup>
          </div>

          <div className="mb-4">
            <h3 className="text-lg font-semibold mb-2">Special Instructions</h3>
            <Textarea
              placeholder="E.g. No onions please"
              value={specialInstructions}
              onChange={(e) => setSpecialInstructions(e.target.value)}
            />
          </div>

          <Button className="w-full">Add to Order - ${item.price.toFixed(2)}</Button>
        </CardContent>
      </Card>
    </div>
  )
}