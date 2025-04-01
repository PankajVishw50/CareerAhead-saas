import { LoaderCircle } from "lucide-react"

const Spinner = ({spinning,  size=24, className}) => {

    return (
        <LoaderCircle
        size={size}
        className={
          "text-white " + className + " " + (
            spinning ? "animate-spin" : ""
          ) + " " + (
            spinning ? "flex" : "hidden"
          )
        }
        />
    )

}



export default Spinner;
