import { LocalDBContent } from "@/context/LocalDBContext"
import { useContext } from "react"

const useLocalDB = () => {
  return useContext(LocalDBContent);
}

export default useLocalDB;
