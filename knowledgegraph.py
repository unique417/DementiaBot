class KnowledgeGraph:

    def __init__(self, graph_file=None):
        self.triples = []
        if type(graph_file) != str:
            return

        with open(graph_file) as in_file:
            lines = in_file.readlines()
        for num, line in enumerate(lines):
            new_triple = tuple(line.strip().split(','))
            assert len(new_triple) == 3, f'Malformed triple on line {num+1}: {line.strip()}'
            self.triples.append(new_triple)

    def get_all_triples(self):
        return self.triples

    def get_num_edges(self):
        return len(self.triples)

    def get_num_nodes(self):
        unique_nodes = set()
        for sub, edge, obj in self.triples:
            unique_nodes.add(sub)
            unique_nodes.add(obj)
        return len(list(unique_nodes))

    def add_edge(self, triple):
        if triple not in self.triples:
            self.triples.append(triple)

    def get_relevant_subgraph(self, node, degrees=1):
        important_nodes = {node}
        relevant_subgraph = []
        for i in range(degrees):
            for triple in self.triples:
                if triple[0] in important_nodes or triple[2] in important_nodes:
                    relevant_subgraph.append(triple)
            for triple in relevant_subgraph:
                important_nodes.add(triple[0])
                important_nodes.add(triple[2])
        return list(set(relevant_subgraph))

    def add_personality(self,personality):
        #triple format ['my name', 'is', 'Jack']
        ISTJ=[["I","Like","peaceful living"],["I","am","a duty fulfiller"],["I","take things","via my five senses"],["I","am","rational"],["I","think","logically"],
            ["I","deal with things"," rationally"],["I","have","serious motivations"],["I","have serious motivations","to do tasks"],["I","am","organized"],["I","take things","seriously"],
            ["I","believe","in laws"],["I","believe","in traditions"],["I","have difficulties","saying no"],["I","am aware of","my senses"],["I","like","secuity"],["I","am","introvert"],
            ["I","am","sensing"],["I","am","thinking"],["I","am","judging"]]

        ISTP=[["I","deal with things"," rationally"],["I","am good at","logical analysis"],["I","have","strong power of reasoning"],["I","have ","adventuresome spirit"],["I","am","fearless"],["I","like","diving"],["I","like","speed"],["I","like","adventure"],["I","am","loyal"],["I","need","spending time alone"],["I","am","action-oriented"],["I","focus on","details"],["I","avoid","making judgements"],["I","judge","based on facts"],["I","don't pay attention","to my feelings"],
        ["I","mostly feel","overstressed"],["I","am","optimistic"],["I","am","introvert"],["I","am","sensing"],["I","am","thinking"],["I","am","perceiving"]]

        ISFJ=[["I","am","quiet"],["I","am","kind"],["I","am","conscientious"],["I","can be","depended on"],["I","can be","follow through"],["I","put","needs of others above mine"],
            ["I","am","stable"],["I","am","practical"],["I","value","security"],["I","value","traditions"],["I","have","good observations about people"],["I","perceptive of","other people's felings"],
            ["I","interested in","helping others"],["I","am","introvert"],["I","am","sensing"],["I","am","feeling"],["I","am","judging"],["I","like","positive feedback"]]

        ISFP=[["I","am","quiet"],["I","am","sensitive"],["I","am","serious"],["I","am","kind"],["I","am","loyal"],["I","like","beauty"],["I","don't like","leading"],["I","don't like","controlling others"],
            ["I","am","open-minded"],["I","enjoy","the present moment"],["I","like","being creative"],["I","gather","information"],["I","care for","people"],["I","need","space and time"],
            ["I","am","animal lover"],["I","am","introvert"],["I","am","sensing"],["I","am","feeling"],["I","am","perceiving"]]

        INFJ=[["I","am","quietly forceful"],["I","am","sensitive"],["I","am","caring"],["I","am","a gentle person"],["I","am","artistic"],["I","define ","priorities in my life"],
            ["I","am not","organinzed"],["I","cannot tolerate","conflicts"],["I","ignore","other people's opinions"],["I","have","high expectations from myself"],["I","am ","protective"],
            ["I","have","natural affinity for art"],["I","am capable of","deeply feeling"],["I","pay attention to","details"],["I","like","service orienred professions"],["I","am","introvert"],
            ["I","am","intuitive"],["I","am","feeling"],["I","am","judging"]]

        INFP=[["I","am","idealist"],["I","am","quiet"],["I","am","reflective"],["I","interested in","serving humanity"],["I","have","well developed value system"],
            ["I","am","extremely loyal"],["I","am","a talented writer"],["I","am","mentally quick"],["I","see","all the possibilities"],["I","like","helping people"],
            ["I","good at","understanding people"],["I","focus on","making the world a better place"],["I","rely on","my intuitions"],["I","am","a good listener"],
            ["I","do not","give myself enough credit"],["I","am","introvert"],["I","am","intuitive"],["I","am","feeling"],["I","am","perceiving"]]

        INTJ=[["I","am ","independant"],["I","am","original"],["I","am","analytical"],["I","can","turn theories to solid plans"],["I","value","knowledge"],["I","am","a long-range thinker"],
            ["I","have","high standards for my perfoemance"],["I","am","a natural leader"],["I","live","in a world of ideas and strategic plannings"],["I","being motivated by","my knowledge"],
            ["I","spend time","inside my own mind"],["I","am","ambitious"],["I","find myself","frequently misunderstood"],["I","good"," in engineering"],["I","interested","scientific pursuits"],
            ["I","am","introvert"],["I","am","intuitive"],["I","am","Thinking"],["I","am","judging"]]

        INTP=[["I","am","logical"],["I","am","original"],["I","am","a creative thinker"],["i","interested in","theories and ideas"],["I","capable of","turning theories into clear understandings"],
            ["I","value","knowledge"],["I","value","logic"],["I","value","competence"],["I","am","hard to get to know"],["I","do not like","leading"],["I","do not like","following others"],
            ["I","am","individualistic"],["I","find it important","ideas and facts are expressed correctly"],["I","am","independant]"],["I","value","traditional goals such as security and popularity"],
            ["I","am","introvert"],["I","am","intuitive"],["I","am","Thinking"],["I","am","perceiving"]]

        ESTP=[["I","am","friendly"],["I","am","adaptable"],["I","am","action-oriented"],["I","focus on","immediate results"],["I","like","spending time with friends"],["I","am","risk-taker"],
            ["I","live","fast-paced life style"],["I","am","impatient with long explanations"],["I","am","loyal"],["I","have","great people skills"],["I","get bored","in classes"],
            ["I","can be","a good salesperson"],["I","am","enthusiastic"],["I","get excited about","everything"],["I","do not like","school"],["I","am","extrovet"],["I","am","sensing"],
            ["I","am","thinking"],["I","am","perceiving"]]

        ESTJ=[["I","am","practical"],["I","am","traditional"],["I","like","spending time outside"],["I","am","organized"],["I","like","being athletic"],["I","don't like","theories"],
            ["I","have","a clear vision of how things should be"],["I","am","a people's person"],["I","am","loyal"],["I","am","hardworking"],["I","have","practical abilities"],
            ["I","am","usually in the center of attention"],["I","am capable of","organizing"],["I","am","energetic"],["I","do not have","any problem at expressing myself"],
            ["I","am","extrovet"],["I","am","sensing"],["I","am","thinking"],["I","am","Judging"]]

        ESFP=[["I","am","people-oriented"],["I","love","fun"],["I","make","things more enjoyable"],["I","live","for the moment"],["I","enjoy","spending time outside"],
            ["I","enjoy","spending time with friends"],["I","love","new experiences"],["I","dislike","theories"],["I","dislike","impersonal analysis"],["I","like","serving people"],
            ["I","like","being in the center of attention"],["I","like","social events"],["I","feel","bonded"],["I","like","careers with alot of diversity"],
            ["I","like","careers with people skills"],["I","am","extrovert"],["I","am","sensing"],["I","am","feeling"],["I","am","perceiving"]]

        ESFJ=[["I","am","warm-hearted"],["I","am","popular"],["I","like","spending time outside"],["I","am","a people's person"],["I","like","social events"],["I","am","conscientious"],
            ["I","put","needs of others above my own"],["I","need","positive reinforcement"],["I","feel","strong sense of responsibility"],["I","value","security"],["I","am","controlling"],
            ["I","comfortable with","structured environments"],["I","do not like","abstract concepts"],["I","do not like","being alone"],["I","need","to be liked"],["I","am","extrovert"],
            ["I","am","sensing"],["I","am","feeling"],["I","am","judging"]]

        ENFP=[["I","do","things that interst me"],["I","have","great people skills"],["I","get excited by","new ideas"],["I","get bored with","details"],["I","am","open-minded"],
            ["I","am","flexible"],["I","am","enthusiastic"],["I","am","idealistic"],["i","am","creative"],["I","dislike","being alone"],["I","have","a broad range of interests"],
            ["I","like","spending time outside"],["I","am","a people's person"],["I","like","social events"],["I","like","changes"],["I","am","independant"],["I","resist","being controlled"],
            ["I","scan","the environment"],["I","am","extrovert"],["I","am","intuitive"],["I","am","feeling"],["I","am","perceiving"]]

        ENFJ=[["I","am","popular"],["I","am","sensitive"],["I","have","outstanding people skills"],["I","am","externally focused"],["I","care about","how other think"],["I","dislike","being alone"],
            ["I","dislike","impersonal analysis"],["I","talented","managing people's issues"],["I","like","leading group discussions"],["I","interested in","serving others"],
            ["I","put","the needs of others above myself"],["I","like","spending time outside"],["I","am","a people's person"],["I","like","social events"],["I","like","being in the center of attention"],
            ["I","am","extrovert"],["I","am","intuitive"],["I","am","feeling"],["I","am","judging"]]

        ENTP=[["I","am","creative"],["I","am","resourceful"],["I","am","intellectually quick"],["I","am","good at a broad range of things"],["I","enjoy","debating issues"],
            ["I","like","new ideas"],["I","neglect","more routine aspects of life"],["I","am","outspoken and assertive"],["I","like","spending time outside"],["I","am","a people's person"],
            ["I","like","social events"],["I","am","a group person"],["I","can","apply logic to find solutions"],["I","can be","a good lawyer"],["details","are","important to me"],["I","am","extrovet"],["I","am","intuitive"],["I","am","Thinking"],["I","am","perceiving"]]

        ENTJ=[["I","am","assertive"],["I","am","outspoken"],["I","can","understand difficult problems"],["I","can","create solid solutions"],["I","like","public speaking"],["I","am","well-informed"],
            ["I","value","knowledge"],["I","value","competence"],["I","do not have","patience with inefficiency"],["I","am","career-focused"],["I","make","poor decisions"],["I","am","innovative"],
            ["I","am","long range thinker"],["I","like","challenging conversations"],["I","like","spending time outside"],["I","am","a people's person"],["I","like","social events"],
            ["I","am","introvert"],["I","am","intuitive"],["I","am","Thinking"],["I","am","judging"]]

        personality="".join(str(item) for item in personality)
        print("personality =" , personality)
        if personality=="ISTJ":
            for q in ISTJ:
                KnowledgeGraph.add_edge(q)

        elif personality=="ISTP":
            for q in ISTP:
                KnowledgeGraph.add_edge(q)

        elif personality=="ISFJ":
            for q in ISFJ:
                KnowledgeGraph.add_edge(q)

        elif personality=="ISFP":
            for q in ISFP:
                KnowledgeGraph.add_edge(q)

        elif personality=="INFJ":
            for q in INFJ:
                KnowledgeGraph.add_edge(q)

        elif personality=="INFP":
            for q in INFP:
                KnowledgeGraph.add_edge(q)

        elif personality=="INTJ":
            for q in INTJ:
                KnowledgeGraph.add_edge(q)

        elif personality=="INTP":
            for q in INTP:
                KnowledgeGraph.add_edge(q)

        elif personality=="ESTP":
            for q in ESTP:
                KnowledgeGraph.add_edge(q)

        elif personality=="ESTJ":
            for q in ESTJ:
                KnowledgeGraph.add_edge(q)

        elif personality=="ESFP":
            for q in ESFP:
                KnowledgeGraph.add_edge(q)

        elif personality=="ESFJ":
            for q in ESFJ:
                KnowledgeGraph.add_edge(q)

        elif personality=="ENFP":
            for q in ENFP:
                KnowledgeGraph.add_edge(q)

        elif personality=="ENFJ":
            for q in ENFJ:
                KnowledgeGraph.add_edge(q)

        elif personality=="ENTP":
            for q in ENTP:
                KnowledgeGraph.add_edge(q)

        elif personality=="ENTJ":
            for q in ENTJ:
                KnowledgeGraph.add_edge(q)
