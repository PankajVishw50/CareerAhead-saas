import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import useColorMode from "@/hooks/useColorMode";
import { Sun, Moon } from "lucide-react";


const ThemeModeToggle = ({className, props}) => {
  const {mode, toggleMode} = useColorMode();

  return (
    <div className={cn(className)} {...props}>
      <Button variant="ghost"
      onClick={() => {
        toggleMode();
      }}
      >
        {
          mode == "dark" ? <Sun />
          : <Moon/>
        }
      </Button>
    </div>
  )
}
export default ThemeModeToggle
