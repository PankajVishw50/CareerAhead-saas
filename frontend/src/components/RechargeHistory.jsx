import useWallet from "@/hooks/useWallet";
import { get_array_index, paise_to_rupees } from "@/utils/collections";
import { useEffect, useState } from "react";

import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination"
import Spinner from "./ui/Spinner";

import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableFooter,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { useToast } from "@/hooks/use-toast";


const RechargeHistory = () => {
  const {toast} = useToast();

  const { recharges, fetch_recharge, setRecharges } = useWallet();
  const [isSearching, setIsSearching] = useState(false);
  const [page, setPage] = useState(1);
  const [size, setSize] = useState(10);
  const [maxPage, setMaxPage] = useState(null);
  const [si, ei] = get_array_index(page, size);

  useEffect(() => {
    if (recharges.length > si){
      return;
    }
    get_recharges(0);
  }, [recharges]);

  const get_recharges = async (direction = 1) => {
    // D = 1 = Forward
    // D = -1 = Back
    // D = 0 = Refresh
    let p = page;

    // Direction
    if (direction == -1) {
      // Previous page
      if (p <= 1) {
        return;
      }
      p -= 1;
    } else if (direction == 1) {
      // Next Page
      p += 1;
    } else if (direction == 0) {
      const [si, ei] = get_array_index(page, size);
      if (recharges.length > si) {
        return;
      }
    }

    if (maxPage && maxPage <= p) {
      return;
    }

    // Check if data is already there
    const [xsi, xei] = get_array_index(p, size);
    if (recharges.length > xsi) {
      setPage(p);
      return;
    }

    // Search
    setIsSearching(true);
    const { response, json, error } = await fetch_recharge(p, size);
    setIsSearching(false);

    if (error) {
      if (response.status_code === 404){
        if (p < maxPage){
          setMaxPage(p);
        }
      }
      return toast({
        description: "Failed to fetch page",
        variant: "destructive",
      });
    }


    setRecharges(prev => {
      const recharge_ids = new Set(prev.map(item => item.id))
      const filtered_r = json.items.filter((recharge) => {
        return !recharge_ids.has(recharge.id)
      })
      return [...prev, ...filtered_r]
    });
    setPage(p);
    setMaxPage(json.totalPages);
  }

  return (
    <div>
      <div>
        <Table>
          <TableCaption>A list of your recent Recharges.</TableCaption>
          <TableHeader>
            <TableRow>
              <TableHead className="w-[100px]">Invoice</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Currency</TableHead>
              <TableHead className="text-right">Amount</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {recharges.length > si && recharges.slice(si, ei).map((recharge) => (
              <TableRow key={recharge.order_id}>
                <TableCell className="font-medium">{recharge.order_id}</TableCell>
                <TableCell>{recharge.status}</TableCell>
                <TableCell>{recharge.currency}</TableCell>
                <TableCell className="text-right">{paise_to_rupees(recharge.amount)}</TableCell>
              </TableRow>
            ))}
          </TableBody>
          {/* <TableFooter>
            <TableRow>
              <TableCell colSpan={3}>Total</TableCell>
              <TableCell className="text-right">$2,500.00</TableCell>
            </TableRow>
          </TableFooter> */}
        </Table>
      </div>
      <div>
        <Pagination
          className="justify-end"
        >
          <PaginationContent>
            <PaginationItem>
              <PaginationPrevious
                to={"#"}
                onClick={(e) => {
                  e.preventDefault();
                  if (isSearching){
                    return;
                  }
                  get_recharges(-1)
                }}
                className="dark:text-white hover:dark:bg-gray-700"
              />
            </PaginationItem>
            <PaginationItem>
              <PaginationLink
                isActive={true}
                to={"/market"}
                className="dark:text-white dark:border dark:border-gray-400 hover:dark:bg-gray-700"
              >
                {
                  isSearching ?
                  <Spinner spinning={isSearching}/>
                  : page
                }
              </PaginationLink>
            </PaginationItem>
            <PaginationItem>
              <PaginationNext
                to={"#"}
                onClick={(e) => {
                  e.preventDefault();
                  if (isSearching){
                    return;
                  }
                  get_recharges(1);
                }}
                className="dark:text-white hover:dark:bg-gray-700"
              />
            </PaginationItem>
          </PaginationContent>
        </Pagination>
      </div>
    </div>
  )
}

export default RechargeHistory;
