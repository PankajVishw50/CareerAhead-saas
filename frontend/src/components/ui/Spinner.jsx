import { LoaderCircle } from "lucide-react"
import {cn} from "@/lib/utils"; 

const Spinner = ({spinning,  size=24, className}) => {

    return (
        <LoaderCircle
        size={size}
        className={cn("text-white", className, spinning ? "animate-spin flex" : "hidden")}
        />
    )

}



export default Spinner;
