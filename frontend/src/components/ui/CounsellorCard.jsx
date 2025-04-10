import dummycounsellor from "@/assets/images/dummycounsellor.jpg"

import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import {NavLink} from "react-router";

export default function CounsellorCard({ counsellor }) {
  return (
    <Card className="p-4 pb-2 shadow-lg rounded-2xl border border-gray-200 w-min min-w-[400px]">
      <div className="flex items-center gap-4">
        <Avatar className="w-20 h-20">
          <AvatarImage src={dummycounsellor} alt={"Pankaj"} />
        </Avatar>
        <div className="flex-1">
          <h2 className="text-xl font-semibold">{counsellor.user.name}</h2>
          <p className="text-gray-700 text-xs font-mediu bg-gray-100 px-1 py-0 rounded-md inline-block">{"G: " + (counsellor.user.gender ?? "other")}</p>
          <p className="text-gray-500 text-sm">Age: {counsellor.user?.age | 18} | Experience: {counsellor?.experience | "3"}+ years</p>
          <div className="flex flex-wrap gap-2 mt-2">
            {["child", "marriage", "alcohol"].map((spec, index) => (
              <Badge key={index}>{spec}</Badge>
            ))}
          </div>
        </div>
      </div>
      <CardContent className="mt-4">
        <p className="text-gray-600 text-sm line-clamp-3 overflow-hidden">
          {
            "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quaerat nisi deleniti accusantium quisquam neque velit aperiam non maiores voluptatem dicta tenetur voluptates consequatur corporis harum, ipsa odio doloribus sequi totam! " +
            "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quaerat nisi deleniti accusantium quisquam neque velit aperiam non maiores voluptatem dicta tenetur voluptates consequatur corporis harum, ipsa odio doloribus sequi totam!"
          }
          {
            "my name is pankaj"
          }
        </p>

        <div className="mt-4 flex justify-between text-sm font-medium">
          <span>Min: ${100}</span>
          <span>Max: ${999}</span>
        </div>
        <Button className="mt-4 w-full" asChild>
          <NavLink to={`/counsellors/${counsellor.id}`} >View Profile</NavLink>
        </Button>
      </CardContent>
    </Card>
  );
}
