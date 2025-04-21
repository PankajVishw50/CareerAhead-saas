import { useParams } from "react-router"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { SquareUser, School, PencilRuler, SquareM } from 'lucide-react';

import {cn} from "@/lib/utils";

import {
  Tabs,
  TabsList,
  TabsTrigger,
  TabsContent
} from "@/components/ui/tabs"

import TestCounter from "@/components/TestCounter";
import { useEffect, useState } from "react";
import useLocalDB from "@/hooks/useLocalDB";
import useAuth from "@/hooks/useAuth";
import { urls } from "@/utils/urls";
import CounsellorScheduleWindow from "@/components/CounsellorScheduleWindow"
import { toast } from "@/hooks/use-toast";

const CounsellorPostPage = () => {
  const {counsellor_id} = useParams();
  const {counsellors, setCounsellors} = useLocalDB();
  const {auth_request} = useAuth();

  const [counsellor, setCounsellor] = useState();
  const [activeTab, setActiveTab] = useState("tab2");

  useEffect(() => {
    // Check if counsellor is available in LocalD
    if (counsellors[counsellor_id]) {
      setCounsellor(counsellors[counsellor_id]);
      return;
    }

    // Fetch it from API
    (async () => {
      const {json, error} = await auth_request(
        urls.counsellor.get_url(counsellor_id),
        {
          method: "GET",
        }
      );

      if (error) {
        toast({
          description: "Failed to fetch counsellor",
          variant: "destructive"
        });
        return
      }

      setCounsellor(json);
      // Save to LocalDB
      setCounsellors(prev => {
        return {
          ...prev,
          [counsellor_id]: json
        }
      });
    })()


  }, [counsellors[counsellor_id]])

  return (
    <Card className="w-full mx-auto rounded-xl border border-muted">
      <CardContent className="p-6">
        <div className="flex items-center gap-4 border-b pb-4 mb-4">
          <Avatar className="h-16 w-16">
            <AvatarImage src="/placeholder.jpg" alt="Dr. Ahmed Khurana" />
            <AvatarFallback>{counsellor ? counsellor.user.name[0].toUpperCase() : "|" }</AvatarFallback>
          </Avatar>
          <div className="text-lg font-medium text-white">
            {counsellor ? counsellor.user.name : "......"}
          </div>
        </div>

        {/* Tabs Section */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid grid-cols-4 gap-2 w-fit mx-auto">
            <TabsTrigger value="tab1">About</TabsTrigger>
            <TabsTrigger value="tab2">Schedule</TabsTrigger>
            <TabsTrigger value="tab3">Review</TabsTrigger>
            <TabsTrigger value="tab4">Q/A</TabsTrigger>
          </TabsList>

          <TabsContent value="tab1" forceMount={true} className={cn("mt-6 text-muted-foreground", activeTab === "tab1" && counsellor ? "" : "hidden")}>

            <div className="p-6 md:p-10 shadow rounded-xl space-y-4">
              <section className="space-y-2 border-b border-dashed border-gray-300 pb-4">
                <div className="flex items-center gap-2">
                  <SquareUser/>
                  <h2 className="text-2xl font-bold text-primary">Introduction</h2>
                </div>
                <p className="text-muted-foreground text-base leading-relaxed">
                  Hello! I'm a dedicated counselor committed to helping individuals find the right direction in life, career, and education. With years of hands-on experience working with students and professionals alike, I believe in listening deeply and guiding patiently. My aim is not to dictate your journey but to help you explore possibilities, overcome barriers, and build a future that feels both practical and fulfilling.
                </p>
              </section>

              <section className="space-y-2 border-b border-dashed border-gray-300 pb-4">
                <div className="flex items-center gap-2">
                  <School/>
                  <h2 className="text-2xl font-bold text-primary">Qualification</h2>
                </div>
                <p className="text-muted-foreground text-base leading-relaxed">
                  Though my formal education includes completing the 10th grade, I have immersed myself in extensive self-learning, mentorship, and on-field counseling. Life experience, combined with ongoing personal development, has shaped my unique perspective on career growth and personal development.
                </p>
              </section>

              <section className="space-y-2 border-b border-dashed border-gray-300 pb-4">
                <div className="flex items-center gap-2">
                  <PencilRuler/>
                  <h2 className="text-2xl font-bold text-primary">Speciality</h2>
                </div>
                <p className="text-muted-foreground text-base leading-relaxed">
                  My strength lies in simplifying complex thoughts, bringing clarity to confused minds, and building trust through open and honest communication. I specialize in guiding those at a crossroads, helping them uncover their true aspirations and create actionable plans.
                </p>
              </section>

              <section className="space-y-2 border-b border-dashed border-gray-300 pb-4">
                <div className="flex items-center gap-2">
                  <SquareM/>
                  <h2 className="text-2xl font-bold text-primary">Methodology</h2>
                </div>
                <p className="text-muted-foreground text-base leading-relaxed">
                  I use the best and most tested tools available—both traditional and modern techniques—to assess and advise. Whether it's psychometric tests, one-on-one dialogue, or tailored action plans, my approach is holistic and client-centered.
                </p>
              </section>
            </div>

          </TabsContent>
          <TabsContent value="tab2" forceMount={true} className={cn("mt-6 text-muted-foreground", activeTab === "tab2" ? "" : "hidden")}>
            { counsellor && <CounsellorScheduleWindow counsellor={counsellor} /> }
          </TabsContent>
          <TabsContent value="tab3" forceMount={true} className={cn("mt-6 text-muted-foreground", activeTab === "tab3" ? "" : "hidden")}>
            <TestCounter/>
          </TabsContent>
          <TabsContent value="tab4" forceMount={true} className={cn("mt-6 text-muted-foreground", activeTab === "tab4" ? "" : "hidden")}>
            Content for Tab 4
          </TabsContent>
        </Tabs>

      </CardContent>
    </Card>
  )
}

export default CounsellorPostPage
