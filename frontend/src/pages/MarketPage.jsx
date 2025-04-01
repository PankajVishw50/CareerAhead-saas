import { ChevronsUpDown } from "lucide-react"

import { Button } from "@/components/ui/button"
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible"


import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { useEffect, useRef, useState } from "react"

import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination"


import { Slider } from "@/components/ui/slider";
import { Label } from "@/components/ui/label";
import { PersonStanding, CircleDollarSign } from "lucide-react";
import { Badge } from "@/components/ui/badge"
import { Checkbox } from "@/components/ui/checkbox"
import Spinner from "@/components/ui/Spinner"

import { Search } from "lucide-react"
import { urls } from "@/utils/urls";


import {
  SidebarGroup,
  SidebarGroupContent,
  SidebarInput,
} from "@/components/ui/sidebar"

import useAuth from "@/hooks/useAuth";
import useRequest from "@/hooks/useRequest"
import CounsellorCard from "@/components/ui/CounsellorCard"

import { SHA256 } from "crypto-js"
import { get_array_index } from "@/utils/collections"

const MarketPage = () => {
  const {auth_request } = useAuth();
  const {get_url_query_params_string} = useRequest();

  const [isOpen, setIsOpen] = useState(false);
  const [isSearching, setIsSearching] = useState(false);
  const firstRender = useRef(true);
  const [counsellors, setCounsellors] = useState({});
  const [page, setPage] = useState(1);
  const [size, setSize] = useState(10);
  const [maxPage, setMaxPage] = useState(false);
  const [csi, cei] = get_array_index(page, size);
  const [filters, setFilters] = useState({
    name: "",
    gender: "all",
    order_by: "none",
    age: null,
    fee: null,
    age_check: false,
    fee_check: false,
  });
  const [params, setParams] = useState({});

  const hash = useRef();
  const timeout = useRef(null);

  useEffect(() => {
    const p = process_filters();
    setParams(process_filters());
    hash.current = SHA256(JSON.stringify(p)).toString();
  }, [filters]);

  useEffect(() => {
    if (firstRender.current){
      return;
    }

    if (timeout.current){
      clearTimeout(timeout.current)
    }

    timeout.current = setTimeout(() => search_counsellors(0, true), 500);
    
    return () => {
      if (timeout.current){
        clearTimeout(timeout.current)
      }
    }
  }, [params]);

  useEffect(() => {
    firstRender.current = false;
  }, [])


  const handleFilter = (e) => {
    // if (isSearching){
    //   return;
    // }
    // console.log(e)
    setFilters(prev => {
      return {
        ...prev,
        [e.target.name]: e.target.value,
      }
    })
  }

  const search_counsellors = async (direction=0, reset=false) => {
    let p = page;

    if (isSearching){
      return;
    }

    if (reset){
      p = 1;
    }

    // Direction
    if (direction == -1){
      if (p <= 1){
        return console.warn("can't go back");
      }
      p -= 1;
    } else if (direction == 1){
      // TODO:Need to fix this}
      if (maxPage !== false & maxPage <= p){
        return console.warn("no next page");
      }
      p += 1;
    }


    let items = [];

    // Check if there is already data
    const [si, ei] = get_array_index(p, size);

    if (counsellors[hash.current] && counsellors[hash.current].items.length > si){
      items = counsellors[hash.current].items.slice(si, ei);
      setMaxPage(counsellors[hash.current].maxPage);
    } else {
      setIsSearching(true);
      const {json, error} = await auth_request(
        get_url_query_params_string(urls.counsellors.get_url(), {...params, page: p, size}),
        {
          method: "GET",
        }
      )

      if (error){
        console.warn("Failed to search counsellor: ", error);
        return;
      }

      items = json.items;
      setCounsellors(prevD => {
        return {
          ...prevD,
          [hash.current]: {
            maxPage: json.totalPages,
            items: [...(prevD[hash.current] ? prevD[hash.current].items : []), ...items]
          } 
        }
      });
      setMaxPage(json.totalPages);
      setIsSearching(false);
    }


    if (direction != 0 | reset){
      setPage(p);
    }

    // Clear timeout
    timeout.current = null;

  }

  const process_filters = () => {
    const params = {
    }

    // Name
    if (filters.name){
      params.name = filters.name;
    }

    // Gender
    if (!["all", "none", null].includes(filters.gender)){
      params.gender = filters.gender;
    }

    // Sort by
    if (!["all", "none", null].includes(filters.sort_by)){
      params.sort_by = filters.sort_by;
    }

    // Fee
    if (filters.fee_check){
      params.min_fee = filters.fee;
    }

    // Age
    if (filters.age_check){
      params.min_age = filters.age;
    }

    return params;


  }


  return (
    <div>
      <div className="container mx-auto px-6 py-6 text-white rounded-xl border bg-card text-card-foreground shadow flex flex-col gap-5">
        <div className="flex flex-row gap-2">
          <div className="height-full flex items-center">
            <SidebarGroup className="py-0 p-0">
              <SidebarGroupContent className="relative">
                <Label htmlFor="name" className="sr-only">
                  Search
                </Label>
                <SidebarInput
                  id="name"
                  placeholder="Type name..."
                  className="pl-8 h-max"
                  name="name"
                  value={filters.name}
                  onChange={handleFilter}
                />

                <Search className="pointer-events-none absolute left-2 top-1/2 size-4 -translate-y-1/2 select-none opacity-50" />
              </SidebarGroupContent>
            </SidebarGroup>
          </div>

          <div>
              <Select name="gender" onValueChange={(val) => handleFilter({target: {name: "gender", value: val}})} value={filters.gender}>
                <SelectTrigger className="w-[150px]">
                  <SelectValue placeholder="Gender" />
                </SelectTrigger>
                <SelectContent>
                  <SelectGroup>
                    <SelectLabel>Genders</SelectLabel>
                    <SelectItem value="all">All</SelectItem>
                    <SelectItem value="male">Male</SelectItem>
                    <SelectItem value="female">Female</SelectItem>
                    <SelectItem value="other">Other</SelectItem>
                  </SelectGroup>
                </SelectContent>
              </Select>
          </div>

          <div>
              <Select name="order_by" onValueChange={(val) => handleFilter({target: {name: "order_by", value: val}})} value={filters.order_by}>
                <SelectTrigger className="w-[150px]">
                  <SelectValue placeholder="Sort By" />
                </SelectTrigger>
                <SelectContent>
                  <SelectGroup>
                    <SelectLabel>Sort By</SelectLabel>
                    <SelectItem value="none">None</SelectItem>
                    <SelectItem value="fee">Fee</SelectItem>
                    <SelectItem value="age">Age</SelectItem>
                  </SelectGroup>
                </SelectContent>
              </Select>
          </div>

        </div>

        <div className="flex flex-row">
          <Collapsible
            open={isOpen}
            onOpenChange={setIsOpen}
            className="w-full space-y-2"
          >
            <div className="flex items-center justify-between space-x-4 px-4">
              <h4 className="text-sm font-semibold">
                Advanced search
              </h4>
              <CollapsibleTrigger asChild>
                <Button variant="ghost" size="sm">
                  <ChevronsUpDown className="h-4 w-4" />
                  <span className="sr-only">Toggle</span>
                </Button>
              </CollapsibleTrigger>
            </div>
            {/* <div className="rounded-md border px-4 py-2 font-mono text-sm shadow-sm">
              @radix-ui/primitives
            </div> */}
            <CollapsibleContent className="space-y-2 px-4">
              <div className="flex flex-col">
                {/* Label for Slider */}
                <Label className="text-sm font-medium">Fee</Label>

                <div className="flex flex-row gap-5">
                  {/* Rating Input with Star Icon */}
                  <div className="flex items-center justify-center space-x-2 w-min py-3">
                    {/* <Star className="h-4 w-4 text-yellow-500" /> */}
                    <Badge variant="secondary" className="w-15 h-10 gap-1">
                      <span>
                        {filters.fee}
                      </span>
                      <CircleDollarSign size={15} />
                    </Badge>
                  </div>

                  {/* Slider for Rating */}
                  <Slider
                    min={100}
                    max={1000}
                    step={25}
                    value={[filters.fee]}
                    onValueChange={(val) => handleFilter({target: {name: "fee", value: val[0]}}) }
                    className="w-[200px] ml-auto"
                  />

                  <Checkbox className="self-center"
                  name="check_fee"
                  checked={filters.fee_check}
                  onCheckedChange={(val) => handleFilter({target: {name: "fee_check", value: val}})}
                  disabled={true}
                  />
                </div>
              </div>

              <div className="flex flex-col">
                {/* Label for Slider */}
                <Label className="text-sm font-medium">Age</Label>

                <div className="flex flex-row gap-5">
                  {/* Rating Input with Star Icon */}
                  <div className="flex items-center justify-center space-x-2 w-min py-3">
                    {/* <Star className="h-4 w-4 text-yellow-500" /> */}
                    <Badge variant="secondary" className="w-15 h-10 gap-1">
                      <span>
                        {filters.age}
                      </span>
                      <PersonStanding size={15} />
                    </Badge>
                  </div>

                  {/* Slider for Age */}
                  <Slider
                    min={18}
                    max={120}
                    step={2}
                    value={[filters.age]}
                    onValueChange={(val) => handleFilter({target: {name: "age", value: val[0]}}) }
                    className="w-[200px] ml-auto"
                  />

                  <Checkbox className="self-center"
                  name="check_age"
                  checked={filters.age_check}
                  onCheckedChange={(val) => handleFilter({target: {name: "age_check", value: val}})}
                  disabled={true}
                  />
                </div>
              </div>

            </CollapsibleContent>
          </Collapsible>
        </div>

      </div>

      <div>
        {
          isSearching ? (
            <Spinner
            className="w-full m-4 justify-center"
            spinning={isSearching} size={50} />
          )  : (
            <div className="py-5 flex gap-5 flex-wrap justify-center">
              {hash.current && counsellors[hash.current]?.items.slice(csi, cei)?.map((counsellor, index) => {
                return <div key={index}>
                  <CounsellorCard counsellor={counsellor} />
                </div>
              })}
            </div>
          )
        }

        <div
        className="pagination my-2"
        >
          <Pagination
          className="justify-end"
          >
            <PaginationContent>
              <PaginationItem>
                <PaginationPrevious
                to={"#"}
                disabled={true}
                onClick={(e) => {
                  e.preventDefault();
                  search_counsellors(-1)
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
                  {page}
                </PaginationLink>
              </PaginationItem>
              <PaginationItem>
                <PaginationNext
                to={"#"}
                onClick={(e) => {
                  e.preventDefault();
                  search_counsellors(1);
                }}
                className="dark:text-white hover:dark:bg-gray-700"
                />
              </PaginationItem>
            </PaginationContent>
          </Pagination>
        </div>

      </div>


    </div>
  )
}
export default MarketPage
