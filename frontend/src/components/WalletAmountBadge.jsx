import useWallet from "@/hooks/useWallet"
import {NavLink} from "react-router";
import {BadgeIndianRupee} from "lucide-react";
import { paise_to_rupees } from "@/utils/collections";

const WalletAmountBadge = () => {
    const {wallet} = useWallet();

    return (
        <div className="flex border rounded hover:border-green-500 ">
        <NavLink to="/wallet" className="flex text-base items-center px-2 gap-2">
        { wallet ? <><BadgeIndianRupee size={18} /> {paise_to_rupees(wallet.balance)}</>
        : <span className="text-red-500">Balance Not Available</span>  
        }
        </NavLink>
        </div>
    ) 

}

export default WalletAmountBadge;