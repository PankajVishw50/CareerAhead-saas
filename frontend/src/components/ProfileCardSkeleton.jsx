import { cn } from "@/lib/utils"
import { Skeleton } from "./ui/skeleton"

const ProfileCardSkeleton = () => {
  return (
    <Skeleton className={cn(
      "w-full max-w-md border",
      "flex flex-col gap-4 px-4 py-2",
      "rounded-none"
    )}>
      <Skeleton className="h-20 w-20 rounded-full" />
      <Skeleton className="w-full h-20" />
      <Skeleton className="w-full h-10" />
    </Skeleton>
  )
}

export default ProfileCardSkeleton
