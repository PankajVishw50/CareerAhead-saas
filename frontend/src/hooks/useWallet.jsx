import { WalletContext } from "@/context/WalletContext"
import { useContext } from "react"

const useWallet = () => {
    return useContext(WalletContext);
}

export default useWallet;