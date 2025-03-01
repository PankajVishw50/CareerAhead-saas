import {SearchCounsellorForm} from "@/components/search-counsellor-form.jsx"

import { ChevronsUpDown } from "lucide-react"

import { Button } from "@/components/ui/button"
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible"


import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { useState } from "react"

import { Slider } from "@/components/ui/slider";
import { Label } from "@/components/ui/label";
import { PersonStanding, CircleDollarSign } from "lucide-react";
import { Badge } from "@/components/ui/badge"



const MarketPage = () => {
  const [isOpen, setIsOpen] = useState(true );
  const [fee, setFee] = useState(100);
  const [age, setAge] = useState(18);

  return (
    <div>
      <div className="container mx-auto px-6 py-6 text-white rounded-xl border bg-card text-card-foreground shadow flex flex-col gap-5">
        <div className="flex flex-row gap-2">
          <SearchCounsellorForm className="height-full flex items-center" />

          <div>
              <Select>
                <SelectTrigger className="w-[150px]">
                  <SelectValue placeholder="Gender" />
                </SelectTrigger>
                <SelectContent>
                  <SelectGroup>
                    <SelectLabel>Genders</SelectLabel>
                    <SelectItem value="all">All</SelectItem>
                    <SelectItem value="male">Male</SelectItem>
                    <SelectItem value="female">Female</SelectItem>
                    <SelectItem value="other">Other</SelectItem>
                  </SelectGroup>
                </SelectContent>
              </Select>
          </div>

          <div>
              <Select>
                <SelectTrigger className="w-[150px]">
                  <SelectValue placeholder="Sort By" />
                </SelectTrigger>
                <SelectContent>
                  <SelectGroup>
                    <SelectLabel>Sort By</SelectLabel>
                    <SelectItem value="none">None</SelectItem>
                    <SelectItem value="fee">Fee</SelectItem>
                    <SelectItem value="age">Age</SelectItem>
                    {/* <SelectItem value="other">Other</SelectItem> */}
                  </SelectGroup>
                </SelectContent>
              </Select>
          </div>

        </div>

        <div className="flex flex-row">
          <Collapsible
            open={isOpen}
            onOpenChange={setIsOpen}
            className="w-full space-y-2"
          >
            <div className="flex items-center justify-between space-x-4 px-4">
              <h4 className="text-sm font-semibold">
                Advanced search
              </h4>
              <CollapsibleTrigger asChild>
                <Button variant="ghost" size="sm">
                  <ChevronsUpDown className="h-4 w-4" />
                  <span className="sr-only">Toggle</span>
                </Button>
              </CollapsibleTrigger>
            </div>
            {/* <div className="rounded-md border px-4 py-2 font-mono text-sm shadow-sm">
              @radix-ui/primitives
            </div> */}
            <CollapsibleContent className="space-y-2 px-4">
              <div className="flex flex-col">
                {/* Label for Slider */}
                <Label className="text-sm font-medium">Fee</Label>

                <div className="flex flex-row justify-between">
                  {/* Rating Input with Star Icon */}
                  <div className="flex items-center justify-center space-x-2 w-min py-3">
                    {/* <Star className="h-4 w-4 text-yellow-500" /> */}
                    <Badge variant="secondary" className="w-15 h-10 gap-1">
                      <span>
                        {fee}
                      </span>
                      <CircleDollarSign size={15} /> 
                    </Badge>
                  </div>

                  {/* Slider for Rating */}
                  <Slider
                    min={100}
                    max={1000}
                    step={25}
                    value={[fee]}
                    onValueChange={(value) => setFee(value[0])}
                    className="w-[200px] justify-self-end"
                  />
                </div>
              </div>

              <div className="flex flex-col">
                {/* Label for Slider */}
                <Label className="text-sm font-medium">Age</Label>

                <div className="flex flex-row justify-between">
                  {/* Rating Input with Star Icon */}
                  <div className="flex items-center justify-center space-x-2 w-min py-3">
                    {/* <Star className="h-4 w-4 text-yellow-500" /> */}
                    <Badge variant="secondary" className="w-15 h-10 gap-1">
                      <span>
                        {age}
                      </span>
                      <PersonStanding size={15} /> 
                    </Badge>
                  </div>

                  {/* Slider for Age */}
                  <Slider
                    min={18}
                    max={120}
                    step={2}
                    value={[age]}
                    onValueChange={(value) => setAge(value[0])}
                    className="w-[200px] justify-self-end"
                  />
                </div>
              </div>

            </CollapsibleContent>
          </Collapsible>
        </div>

      </div>
    </div>
  )
}
export default MarketPage
