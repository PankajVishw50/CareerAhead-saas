import { Link } from "react-router"
import { Button } from "./ui/button"
import { DribbbleIcon, TwitchIcon, TwitterIcon } from "lucide-react";
import { Separator } from "./ui/separator";
import { cn } from "@/lib/utils";
import { Avatar, AvatarFallback, AvatarImage } from "./ui/avatar";
import { capitalize, get_name_initials } from "@/utils/helpers";

const CounsellorProfile = ({ counsellor }) => {
  return (
    <div className={cn(
      "w-full max-w-md border",
      "flex flex-col gap-4 px-4 py-2",
    )}>
      <div>
        <Avatar className="h-20 w-20 ">
          <AvatarImage src={counsellor.user.image} />
          <AvatarFallback>{get_name_initials(counsellor.user.name)}</AvatarFallback>
        </Avatar>
      </div>

      <div>
        <div className="flex items-center gap-2 h-5">
          <h3 className="text-lg font-semibold">{capitalize(counsellor.user.name)}</h3>
          <Separator orientation="vertical" className="h-full" />
          <p className="text-muted-foreground text-sm">{"Counsellor"}</p>
        </div>
        <div className="mt-2 line-clamp-3">
          {counsellor.about.introduction}
        </div>
      </div>

      <div className="mt-4 flex items-center gap-2.5 mt-auto self-end">
        <Button
          className="bg-accent hover:bg-accent shadow-none"
          // size="icon"
          asChild
        >
          <Link to={`/counsellors/${counsellor.id}`} className="text-muted-foreground text-white text-xs">
            {/* <TwitterIcon className="stroke-muted-foreground" /> */}
            Visit Profile
          </Link>
        </Button>
      </div>
    </div>

  )
}

export default CounsellorProfile

