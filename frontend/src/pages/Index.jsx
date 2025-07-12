import { Button } from "@/components/ui/button"
import SessionsWindow from "@/components/SessionsWindow";

const Index = () => {

  return (
    <div className="flex gap-5">
      <SessionsWindow type="all" params={"?types=all"} />
      <SessionsWindow
        type="upcoming"
        params={"?types=upcoming"}
        background_color="bg-[#57cc99]/10"
        hover_background_color="hover:bg-[#57cc99]/20"
      />
    </div>

  )
}
export default Index
