import { AppSidebar } from "@/components/app-sidebar"
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb"
import { Separator } from "@/components/ui/separator"
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar"
import { Outlet } from "react-router"
import { Sun, Moon, BadgeIndianRupee } from "lucide-react";
import {Button} from "@/components/ui/button"
import useColorMode from "@/hooks/useColorMode"
import ThemeModeToggle from "@/components/ThemeModeToggle"
import { Badge } from "@/components/ui/badge"
import {NavLink} from "react-router";
import {useState} from "react";
import WalletAmountBadge from "@/components/WalletAmountBadge"

export default function DashboardLayout() {
  const {mode, toggleMode} = useColorMode();
  const [headerTitle, setHeaderTitle] = useState("");



  return (
    <SidebarProvider>
      <AppSidebar />

      <SidebarInset>

        <header className="flex h-16 shrink-0 items-center gap-2 transition-[width,height] ease-linear group-has-[[data-collapsible=icon]]/sidebar-wrapper:h-12">
          <div className="flex items-center gap-2 px-4 w-full">
            <SidebarTrigger className="dark:text-white -ml-1" />
            <Separator orientation="vertical" className="mr-2 h-4" />
              <div className="dark:text-white">{headerTitle}</div>
            {/* <Breadcrumb>
              <BreadcrumbList>
                <BreadcrumbItem className="hidden md:block">
                  <BreadcrumbLink href="#">
                    Building Your Application
                  </BreadcrumbLink>
                </BreadcrumbItem>
                <BreadcrumbSeparator className="hidden md:block" />
                <BreadcrumbItem>
                  <BreadcrumbPage>Data Fetching</BreadcrumbPage>
                </BreadcrumbItem>
              </BreadcrumbList>
            </Breadcrumb> */}
            <div className="dark:text-white px-2 py-0 w-full flex justify-end gap-3 items-stretch">
              <WalletAmountBadge/>
              <ThemeModeToggle/>
              {/* <Button variant="outlined"
              onClick={() => {
                toggleMode();
              }}
              >
                {
                  mode == "dark" ? <Sun />
                  : <Moon/>
                }
              </Button> */}
            </div>
          </div>
        </header>

        <div className="flex flex-1 flex-col gap-4 p-4 pt-0">
          <Outlet context={{setHeaderTitle}} />

          {/* Skeleton */}
          {/* <div className="grid auto-rows-min gap-4 md:grid-cols-3">
            <div className="aspect-video rounded-xl bg-muted/50" />
            <div className="aspect-video rounded-xl bg-muted/50" />
            <div className="aspect-video rounded-xl bg-muted/50" />
          </div>
          <div className="min-h-[100vh] flex-1 rounded-xl bg-muted/50 md:min-h-min" /> */}
        </div>
      </SidebarInset>

    </SidebarProvider>
  )
}
