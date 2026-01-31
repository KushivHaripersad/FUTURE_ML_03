import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import pandas as pd
from pathlib import Path
import os
from datetime import datetime
from PIL import Image, ImageTk

# Add project root to path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import DataLoader
from utils.text_processor import TextProcessor
from utils.model_trainer import ModelTrainer
from utils.similarity_scorer import SimilarityScorer
from utils.database_manager import DatabaseManager
from app.theme import AppTheme, ModernUIComponents

class ResumeScreenerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Resume Screening System")
        self.root.geometry("1400x800")
        
        # Apply theme
        self.theme = AppTheme()
        self.theme.apply_theme(root)
        
        # Initialize components
        self.data_loader = DataLoader()
        self.text_processor = TextProcessor()
        self.model_trainer = ModelTrainer()
        self.similarity_scorer = SimilarityScorer()
        self.db_manager = DatabaseManager()
        
        # Data storage
        self.resumes = []
        self.current_jd = ""
        self.ranked_candidates = []
        
        # Load models
        self.load_models()
        
        # Setup enhanced GUI
        self.setup_enhanced_gui()
        
    def load_models(self):
        """Load pre-trained models"""
        model_dir = "models"
        try:
            if os.path.exists(model_dir):
                self.model_trainer.load_models(model_dir)
                print("Models loaded successfully")
            else:
                print("Models directory not found. Please train models first.")
        except Exception as e:
            print(f"Error loading models: {e}")
    
    def setup_enhanced_gui(self):
        """Setup the enhanced GUI layout with modern styling"""
        # Configure main window
        self.root.configure(bg=self.theme.colors['background'])
        
        # Create header
        header_frame = ModernUIComponents.create_header(
            self.root, 
            "AI Resume Screening System",
            "Smart Recruitment Made Easy"
        )
        header_frame.pack(fill='x', padx=20, pady=(15, 10))
        
        # Create main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Create left panel
        left_panel = self.theme.create_card(main_container)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Create right panel
        right_panel = self.theme.create_card(main_container)
        right_panel.pack(side='right', fill='both', expand=True)
        
        # Configure panels
        left_panel.columnconfigure(0, weight=1)
        left_panel.rowconfigure(1, weight=1)
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(1, weight=1)
        
        # Job Description Section (Left Panel)
        jd_header_frame = ttk.Frame(left_panel)
        jd_header_frame.grid(row=0, column=0, sticky='ew', pady=(10, 5))
        
        ttk.Label(jd_header_frame, text="Job Description", 
                 style='Heading.TLabel').pack(side='left')
        
        # JD buttons
        jd_btn_frame = ttk.Frame(jd_header_frame)
        jd_btn_frame.pack(side='right')
        
        ttk.Button(jd_btn_frame, text="Load", 
                  command=self.load_jd_from_file,
                  style='Secondary.TButton').pack(side='left', padx=(0, 5))
        ttk.Button(jd_btn_frame, text="Clear", 
                  command=self.clear_jd,
                  style='Secondary.TButton').pack(side='left')
        
        # JD text area
        jd_text_frame = ttk.Frame(left_panel)
        jd_text_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=(0, 10))
        jd_text_frame.columnconfigure(0, weight=1)
        jd_text_frame.rowconfigure(0, weight=1)
        
        self.jd_text = scrolledtext.ScrolledText(jd_text_frame, 
                                                wrap=tk.WORD,
                                                font=self.theme.fonts['body'],
                                                bg='white',
                                                fg=self.theme.colors['text_primary'],
                                                insertbackground=self.theme.colors['secondary'])
        self.jd_text.grid(row=0, column=0, sticky='nsew')
        
        # Resumes Section (Left Panel)
        resume_header_frame = ttk.Frame(left_panel)
        resume_header_frame.grid(row=2, column=0, sticky='ew', pady=(10, 5))
        
        ttk.Label(resume_header_frame, text="Resume Input", 
                 style='Heading.TLabel').pack(side='left')
        
        # Resume buttons
        resume_btn_frame = ttk.Frame(resume_header_frame)
        resume_btn_frame.pack(side='right')
        
        ttk.Button(resume_btn_frame, text="Single", 
                  command=self.load_word_resume,
                  style='Secondary.TButton').pack(side='left', padx=(0, 5))
        ttk.Button(resume_btn_frame, text="Multiple", 
                  command=self.load_multiple_word_resumes,
                  style='Secondary.TButton').pack(side='left')
        
        # Resume list area
        resume_list_frame = ttk.Frame(left_panel)
        resume_list_frame.grid(row=3, column=0, sticky='nsew', padx=10, pady=(0, 10))
        resume_list_frame.columnconfigure(0, weight=1)
        resume_list_frame.rowconfigure(0, weight=1)
        
        self.resume_listbox = tk.Listbox(resume_list_frame,
                                        font=self.theme.fonts['body'],
                                        bg='white',
                                        fg=self.theme.colors['text_primary'],
                                        selectbackground=self.theme.colors['secondary'],
                                        selectforeground='white')
        self.resume_listbox.grid(row=0, column=0, sticky='nsew')
        
        list_scrollbar = ttk.Scrollbar(resume_list_frame,
                                      orient='vertical',
                                      command=self.resume_listbox.yview)
        list_scrollbar.grid(row=0, column=1, sticky='ns')
        self.resume_listbox.config(yscrollcommand=list_scrollbar.set)
        
        # Database button
        db_btn_frame = ttk.Frame(left_panel)
        db_btn_frame.grid(row=4, column=0, pady=(5, 10))
        
        ttk.Button(db_btn_frame, text="View Database", 
                  command=self.view_database,
                  style='Primary.TButton').pack()
        
        # Results Section (Right Panel)
        results_header_frame = ttk.Frame(right_panel)
        results_header_frame.grid(row=0, column=0, sticky='ew', pady=(10, 5))
        
        ttk.Label(results_header_frame, text="Ranking Results", 
                 style='Heading.TLabel').pack(side='left')
        
        # Stats frame
        stats_frame = ttk.Frame(results_header_frame)
        stats_frame.pack(side='right')
        
        self.stats_label = ttk.Label(stats_frame, text="0 resumes loaded",
                                    style='Subheading.TLabel')
        self.stats_label.pack(side='right')
        
        # Results treeview
        results_tree_frame = ttk.Frame(right_panel)
        results_tree_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=(0, 10))
        results_tree_frame.columnconfigure(0, weight=1)
        results_tree_frame.rowconfigure(0, weight=1)
        
        # Create treeview with columns
        columns = ('Rank', 'Name', 'Category', 'Score', 'Missing Skills')
        self.results_tree = ttk.Treeview(results_tree_frame, 
                                        columns=columns, 
                                        show='headings',
                                        height=15)
        
        # Configure columns
        self.results_tree.heading('Rank', text='Rank', anchor='center')
        self.results_tree.heading('Name', text='Name', anchor='w')
        self.results_tree.heading('Category', text='Category', anchor='w')
        self.results_tree.heading('Score', text='Score', anchor='center')
        self.results_tree.heading('Missing Skills', text='Missing Skills', anchor='center')
        
        self.results_tree.column('Rank', width=60, anchor='center')
        self.results_tree.column('Name', width=150, anchor='w')
        self.results_tree.column('Category', width=120, anchor='w')
        self.results_tree.column('Score', width=80, anchor='center')
        self.results_tree.column('Missing Skills', width=120, anchor='center')
        
        self.results_tree.grid(row=0, column=0, sticky='nsew')
        
        tree_scrollbar = ttk.Scrollbar(results_tree_frame,
                                      orient='vertical',
                                      command=self.results_tree.yview)
        tree_scrollbar.grid(row=0, column=1, sticky='ns')
        self.results_tree.config(yscrollcommand=tree_scrollbar.set)
        
        # Action buttons (Bottom toolbar)
        action_frame = ttk.Frame(self.root)
        action_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        ttk.Button(action_frame, text="Screen & Rank", 
                  command=self.screen_resumes,
                  style='Success.TButton').pack(side='left', padx=(0, 10))
        
        ttk.Button(action_frame, text="Save to Database", 
                  command=self.save_to_database,
                  style='Primary.TButton').pack(side='left', padx=(0, 10))
        
        ttk.Button(action_frame, text="Skill Analysis", 
                  command=self.show_skill_analysis,
                  style='Secondary.TButton').pack(side='left', padx=(0, 10))
        
        ttk.Button(action_frame, text="Clear All", 
                  command=self.clear_all,
                  style='Warning.TButton').pack(side='left')
        
        # Status bar
        status_frame = ttk.Frame(self.root, relief='sunken', borderwidth=1)
        status_frame.pack(side='bottom', fill='x')
        
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Load resumes and enter job description")
        
        status_label = ttk.Label(status_frame, 
                                textvariable=self.status_var,
                                style='Body.TLabel',
                                relief='sunken',
                                padding=5)
        status_label.pack(side='left')
        
        # Progress indicator
        self.progress_var = tk.IntVar()
        progress_bar = ttk.Progressbar(status_frame,
                                      variable=self.progress_var,
                                      length=100,
                                      mode='determinate')
        progress_bar.pack(side='right', padx=(0, 10))
    
    def load_jd_from_file(self):
        """Load job description from text file"""
        file_path = filedialog.askopenfilename(
            title="Select Job Description File",
            filetypes=[("Text files", "*.txt"), ("Word files", "*.docx"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                if file_path.endswith('.docx'):
                    # Extract text from Word document
                    text = self.data_loader.extract_text_from_docx(file_path)
                else:
                    # Read text file
                    with open(file_path, 'r', encoding='utf-8') as file:
                        text = file.read()
                
                self.jd_text.delete(1.0, tk.END)
                self.jd_text.insert(1.0, text)
                self.status_var.set(f"Loaded JD from {Path(file_path).name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")
    
    def clear_jd(self):
        """Clear job description"""
        self.jd_text.delete(1.0, tk.END)
        self.status_var.set("Job description cleared")
    
    def load_word_resume(self):
        """Load a single resume from Word document"""
        file_path = filedialog.askopenfilename(
            title="Select Resume (Word Document)",
            filetypes=[("Word documents", "*.docx"), ("All files", "*.*")]
        )
        
        if file_path:
            self._process_word_resume(file_path)
    
    def load_multiple_word_resumes(self):
        """Load multiple resumes from Word documents"""
        file_paths = filedialog.askopenfilenames(
            title="Select Resumes (Word Documents)",
            filetypes=[("Word documents", "*.docx"), ("All files", "*.*")]
        )
        
        for file_path in file_paths:
            self._process_word_resume(file_path)
    
    def _process_word_resume(self, file_path: str):
        """Process a Word resume file"""
        try:
            # Extract resume info
            resume_info = self.data_loader.extract_resume_info_from_docx(file_path)
            
            if not resume_info.get('text'):
                messagebox.showwarning("Warning", f"No text could be extracted from {Path(file_path).name}")
                return
            
            # Add to resumes list
            self.resumes.append(resume_info)
            
            # Add to listbox
            display_text = f"{resume_info['name']} - {Path(file_path).name}"
            self.resume_listbox.insert(tk.END, display_text)
            
            # Update stats
            self.stats_label.config(text=f"{len(self.resumes)} resumes loaded")
            self.status_var.set(f"Loaded resume: {resume_info['name']}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load resume: {e}")
    
    def screen_resumes(self):
        """Screen and rank resumes"""
        # Get job description
        self.current_jd = self.jd_text.get(1.0, tk.END).strip()
        
        if not self.current_jd:
            messagebox.showwarning("Warning", "Please enter a job description")
            return
        
        if not self.resumes:
            messagebox.showwarning("Warning", "Please load some resumes first")
            return
        
        # Show processing
        self.status_var.set("Processing... Please wait")
        self.progress_var.set(30)
        self.root.update()
        
        try:
            # Prepare resumes for scoring
            resumes_for_scoring = []
            for resume in self.resumes:
                resumes_for_scoring.append({
                    'id': resume.get('name', 'Unknown'),
                    'text': resume.get('text', ''),
                    'category': 'Unknown',
                    'original_data': resume
                })
            
            # Update progress
            self.progress_var.set(60)
            self.root.update()
            
            # Rank candidates
            self.ranked_candidates = self.similarity_scorer.rank_candidates(
                resumes_for_scoring, self.current_jd
            )
            
            # Update progress
            self.progress_var.set(90)
            self.root.update()
            
            # Update results tree
            self.update_results_tree()
            
            # Complete progress
            self.progress_var.set(100)
            self.status_var.set(f"Ranked {len(self.ranked_candidates)} candidates")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to screen resumes: {e}")
            self.status_var.set("Error occurred")
            self.progress_var.set(0)
    
    def update_results_tree(self):
        """Update the results treeview with ranked candidates"""
        # Clear existing items
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Add ranked candidates with color coding
        for candidate in self.ranked_candidates:
            missing_skills = sum(len(skills) for skills in candidate['skill_gaps'].values())
            score = candidate['similarity_score']
            
            # Determine tag based on score
            if score >= 0.8:
                tag = 'excellent'
            elif score >= 0.6:
                tag = 'good'
            elif score >= 0.4:
                tag = 'average'
            else:
                tag = 'poor'
            
            self.results_tree.insert('', tk.END, values=(
                candidate['rank'],
                candidate['id'],
                candidate['category'],
                f"{score:.1%}",
                f"{missing_skills} missing"
            ), tags=(tag,))
        
        # Configure tag colors
        self.results_tree.tag_configure('excellent', background='#D5F4E6')  # Light green
        self.results_tree.tag_configure('good', background='#D6EAF8')      # Light blue
        self.results_tree.tag_configure('average', background='#FCF3CF')   # Light yellow
        self.results_tree.tag_configure('poor', background='#FADBD8')      # Light red
    
    def save_to_database(self):
        """Save ranked candidates to database"""
        if not self.ranked_candidates:
            messagebox.showwarning("Warning", "No ranked candidates to save. Please screen resumes first.")
            return
        
        try:
            saved_count = 0
            for candidate in self.ranked_candidates:
                # Get original resume data
                original_data = candidate['original_data']
                
                # Prepare applicant data
                applicant_data = {
                    'name': original_data.get('name', candidate['id']),
                    'email': original_data.get('email', ''),
                    'phone': original_data.get('phone', ''),
                    'resume_text': original_data.get('text', ''),
                    'file_path': original_data.get('file_path', ''),
                    'category': candidate['category'],
                    'score': candidate['similarity_score'],
                    'missing_skills': ', '.join([
                        f"{cat}: {', '.join(skills)}" 
                        for cat, skills in candidate['skill_gaps'].items()
                    ]),
                    'processed_date': datetime.now(),
                    'skills': self.text_processor.extract_skills(original_data.get('text', ''))
                }
                
                # Save to database
                self.db_manager.add_applicant(applicant_data)
                saved_count += 1
            
            self.status_var.set(f"Saved {saved_count} candidates to database")
            messagebox.showinfo("Success", f"Successfully saved {saved_count} candidates to database")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save to database: {e}")
    
    def view_database(self):
        """Open enhanced database viewer window"""
        db_window = EnhancedDatabaseViewer(self.root, self.db_manager)
        db_window.grab_set()
    
    def show_skill_analysis(self):
        """Show detailed skill analysis for selected candidate"""
        selection = self.results_tree.selection()
        if not selection:
            messagebox.showinfo("Info", "Please select a candidate from the results")
            return
        
        item = self.results_tree.item(selection[0])
        rank = item['values'][0]
        
        # Find the candidate
        candidate = next((c for c in self.ranked_candidates if c['rank'] == rank), None)
        
        if candidate:
            self.show_enhanced_candidate_details(candidate)
    
    def show_enhanced_candidate_details(self, candidate):
        """Show enhanced candidate information"""
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Candidate Analysis: {candidate['id']}")
        details_window.geometry("900x700")
        
        # Apply theme to window
        details_window.configure(bg=self.theme.colors['background'])
        
        # Header
        header_frame = ModernUIComponents.create_header(
            details_window,
            f"Candidate Analysis",
            f"{candidate['id']} - Score: {candidate['similarity_score']:.1%}"
        )
        header_frame.pack(fill='x', padx=20, pady=(15, 10))
        
        # Create notebook for tabs
        notebook = ttk.Notebook(details_window)
        notebook.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Score Analysis Tab
        score_frame = ttk.Frame(notebook)
        notebook.add(score_frame, text="Score Analysis")
        
        # Score cards
        score_cards_frame = ttk.Frame(score_frame)
        score_cards_frame.pack(fill='x', padx=20, pady=20)
        
        # Overall Score Card
        overall_card = self.theme.create_card(score_cards_frame)
        overall_card.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        ttk.Label(overall_card, text="Overall Match Score",
                 style='Subheading.TLabel').pack(pady=(15, 5))
        
        score_font = ('Segoe UI', 36, 'bold')
        score_color = self.theme.colors['success'] if candidate['similarity_score'] >= 0.7 else self.theme.colors['warning'] if candidate['similarity_score'] >= 0.5 else self.theme.colors['accent']
        score_label = tk.Label(overall_card, 
                              text=f"{candidate['similarity_score']:.1%}",
                              font=score_font,
                              fg=score_color,
                              bg=self.theme.colors['card_bg'])
        score_label.pack(pady=(0, 15))
        
        # Category Card
        category_card = self.theme.create_card(score_cards_frame)
        category_card.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        ttk.Label(category_card, text="Predicted Category",
                 style='Subheading.TLabel').pack(pady=(15, 5))
        
        category_label = tk.Label(category_card,
                                 text=candidate['category'],
                                 font=('Segoe UI', 18, 'bold'),
                                 fg=self.theme.colors['text_primary'],
                                 bg=self.theme.colors['card_bg'])
        category_label.pack(pady=(0, 15))
        
        # Missing Skills Card
        missing_card = self.theme.create_card(score_cards_frame)
        missing_card.pack(side='left', fill='both', expand=True)
        
        ttk.Label(missing_card, text="Missing Skills",
                 style='Subheading.TLabel').pack(pady=(15, 5))
        
        missing_label = tk.Label(missing_card,
                                text=str(candidate['missing_skills_count']),
                                font=('Segoe UI', 24, 'bold'),
                                fg=self.theme.colors['accent'],
                                bg=self.theme.colors['card_bg'])
        missing_label.pack(pady=(0, 15))
        
        # Skills Analysis Tab
        skills_frame = ttk.Frame(notebook)
        notebook.add(skills_frame, text="Skills Analysis")
        
        # Extract skills from resume
        resume_skills = self.text_processor.extract_skills(candidate['original_data']['text'])
        
        # Create skill visualization
        skills_container = ttk.Frame(skills_frame)
        skills_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Skills found section
        found_frame = ttk.Frame(skills_container)
        found_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        ttk.Label(found_frame, text="Skills Found",
                 style='Heading.TLabel').pack(anchor='w', pady=(0, 10))
        
        # Create skills grid
        skills_grid = ttk.Frame(found_frame)
        skills_grid.pack(fill='x')
        
        col = 0
        row = 0
        max_cols = 3
        
        for category, skills in resume_skills.items():
            if skills:  # Only show categories with skills
                category_frame = self.theme.create_card(skills_grid)
                category_frame.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
                
                ttk.Label(category_frame, text=category.upper(),
                         style='Subheading.TLabel').pack(pady=(10, 5))
                
                for skill in skills:
                    skill_label = ttk.Label(category_frame, text=f"• {skill}",
                                           style='Body.TLabel')
                    skill_label.pack(anchor='w', padx=10)
                
                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1
        
        # Missing skills section
        if candidate['skill_gaps']:
            missing_frame = ttk.Frame(skills_container)
            missing_frame.pack(fill='both', expand=True)
            
            ttk.Label(missing_frame, text="Missing Skills",
                     style='Heading.TLabel').pack(anchor='w', pady=(0, 10))
            
            missing_grid = ttk.Frame(missing_frame)
            missing_grid.pack(fill='x')
            
            col = 0
            row = 0
            
            for category, skills in candidate['skill_gaps'].items():
                category_frame = self.theme.create_card(missing_grid)
                category_frame.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
                
                ttk.Label(category_frame, text=category.upper(),
                         style='Subheading.TLabel',
                         foreground=self.theme.colors['accent']).pack(pady=(10, 5))
                
                for skill in skills:
                    skill_label = ttk.Label(category_frame, text=f"• {skill}",
                                           style='Body.TLabel',
                                           foreground=self.theme.colors['accent'])
                    skill_label.pack(anchor='w', padx=10)
                
                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1
        
        # Configure grid weights
        for i in range(max_cols):
            skills_grid.columnconfigure(i, weight=1)
            if candidate['skill_gaps']:
                missing_grid.columnconfigure(i, weight=1)
    
    def clear_all(self):
        """Clear all data"""
        self.resumes = []
        self.ranked_candidates = []
        self.current_jd = ""
        
        self.resume_listbox.delete(0, tk.END)
        self.jd_text.delete(1.0, tk.END)
        
        # Clear results tree
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Update stats
        self.stats_label.config(text="0 resumes loaded")
        self.status_var.set("All data cleared")
        self.progress_var.set(0)


class EnhancedDatabaseViewer:
    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        self.window = tk.Toplevel(parent)
        self.window.title("Applicant Database - Advanced View")
        self.window.geometry("1300x700")
        
        # Apply theme
        self.theme = AppTheme()
        self.theme.apply_theme(self.window)
        
        self.setup_enhanced_gui()
        self.load_data()
    
    def setup_enhanced_gui(self):
        """Setup enhanced database viewer GUI"""
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill='both', expand=True)
        
        # Configure grid weights
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Header
        header_frame = ModernUIComponents.create_header(
            main_frame,
            "Applicant Database",
            "Manage and analyze stored resumes"
        )
        header_frame.grid(row=0, column=0, sticky='ew', pady=(0, 15))
        
        # Control panel
        control_frame = self.theme.create_card(main_frame)
        control_frame.grid(row=1, column=0, sticky='ew', pady=(0, 10))
        
        # Search and filter controls
        search_frame = ttk.Frame(control_frame)
        search_frame.pack(fill='x', padx=15, pady=15)
        
        ttk.Label(search_frame, text="Search:",
                 style='Subheading.TLabel').pack(side='left', padx=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_changed)
        search_entry = ttk.Entry(search_frame, 
                                textvariable=self.search_var,
                                width=30,
                                style='Primary.TEntry')
        search_entry.pack(side='left', padx=(0, 20))
        
        ttk.Label(search_frame, text="Min Score:",
                 style='Subheading.TLabel').pack(side='left', padx=(0, 10))
        
        self.min_score_var = tk.DoubleVar(value=0.0)
        min_score_spin = ttk.Spinbox(search_frame, 
                                    from_=0.0, to=1.0,
                                    increment=0.1,
                                    textvariable=self.min_score_var,
                                    width=5,
                                    style='Primary.TEntry')
        min_score_spin.pack(side='left', padx=(0, 20))
        
        # Action buttons
        action_frame = ttk.Frame(control_frame)
        action_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        ttk.Button(action_frame, text="Refresh", 
                  command=self.load_data,
                  style='Secondary.TButton').pack(side='left', padx=(0, 10))
        
        ttk.Button(action_frame, text="Order by Score", 
                  command=self.order_by_score,
                  style='Success.TButton').pack(side='left', padx=(0, 10))
        
        ttk.Button(action_frame, text="Statistics", 
                  command=self.show_enhanced_statistics,
                  style='Primary.TButton').pack(side='left', padx=(0, 10))
        
        ttk.Button(action_frame, text="Export to CSV", 
                  command=self.export_to_csv,
                  style='Secondary.TButton').pack(side='left')
        
        # Treeview for data
        tree_container = ttk.Frame(main_frame)
        tree_container.grid(row=2, column=0, sticky='nsew')
        
        # Configure tree container grid
        tree_container.columnconfigure(0, weight=1)
        tree_container.rowconfigure(0, weight=1)
        
        # Create treeview with scrollbars
        tree_frame = ttk.Frame(tree_container)
        tree_frame.grid(row=0, column=0, sticky='nsew')
        
        # Create horizontal scrollbar first
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        # Create vertical scrollbar
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        
        # Create treeview
        columns = ('ID', 'Name', 'Email', 'Category', 'Score', 'Missing Skills', 'Processed Date')
        self.tree = ttk.Treeview(tree_frame, 
                                columns=columns, 
                                show='headings',
                                xscrollcommand=h_scrollbar.set,
                                yscrollcommand=v_scrollbar.set,
                                height=15)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        
        # Configure scrollbars
        h_scrollbar.config(command=self.tree.xview)
        v_scrollbar.config(command=self.tree.yview)
        
        # Define columns
        self.tree.heading('ID', text='ID', anchor='center')
        self.tree.heading('Name', text='Name', anchor='w')
        self.tree.heading('Email', text='Email', anchor='w')
        self.tree.heading('Category', text='Category', anchor='w')
        self.tree.heading('Score', text='Score', anchor='center')
        self.tree.heading('Missing Skills', text='Missing Skills', anchor='center')
        self.tree.heading('Processed Date', text='Processed Date', anchor='center')
        
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Name', width=180, anchor='w')
        self.tree.column('Email', width=220, anchor='w')
        self.tree.column('Category', width=120, anchor='w')
        self.tree.column('Score', width=80, anchor='center')
        self.tree.column('Missing Skills', width=150, anchor='center')
        self.tree.column('Processed Date', width=150, anchor='center')
        
        # Configure tree frame grid
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, 
                              textvariable=self.status_var,
                              style='Body.TLabel',
                              relief='sunken',
                              padding=5)
        status_bar.grid(row=3, column=0, sticky='ew', pady=(10, 0))
    
    def load_data(self, order_by_score: bool = False):
        """Load data from database"""
        try:
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Get data from database
            df = self.db_manager.get_all_applicants(order_by_score)
            
            if df.empty:
                self.status_var.set("No data in database")
                return
            
            # Add data to treeview with color coding
            for _, row in df.iterrows():
                score = row['score']
                
                # Determine tag based on score
                if score >= 0.8:
                    tag = 'excellent'
                elif score >= 0.6:
                    tag = 'good'
                elif score >= 0.4:
                    tag = 'average'
                else:
                    tag = 'poor'
                
                self.tree.insert('', tk.END, values=(
                    int(row['id']),
                    row['name'],
                    row['email'],
                    row['category'],
                    f"{row['score']:.1%}",
                    f"{len(row['missing_skills'].split(',')) if row['missing_skills'] else 0} skills",
                    row['processed_date']
                ), tags=(tag,))
            
            # Configure tag colors
            self.tree.tag_configure('excellent', background='#D5F4E6')
            self.tree.tag_configure('good', background='#D6EAF8')
            self.tree.tag_configure('average', background='#FCF3CF')
            self.tree.tag_configure('poor', background='#FADBD8')
            
            self.status_var.set(f"Loaded {len(df)} applicants from database")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")
    
    def order_by_score(self):
        """Order applicants by score"""
        self.load_data(order_by_score=True)
        self.status_var.set("Ordered by score (highest first)")
    
    def on_search_changed(self, *args):
        """Handle search text change"""
        keyword = self.search_var.get()
        min_score = self.min_score_var.get()
        
        if keyword or min_score > 0:
            self.perform_search(keyword, min_score)
    
    def perform_search(self, keyword: str, min_score: float):
        """Perform search in database"""
        try:
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Search in database
            df = self.db_manager.search_applicants(keyword, min_score)
            
            if df.empty:
                self.status_var.set("No matching applicants found")
                return
            
            # Add data to treeview
            for _, row in df.iterrows():
                score = row['score']
                
                if score >= 0.8:
                    tag = 'excellent'
                elif score >= 0.6:
                    tag = 'good'
                elif score >= 0.4:
                    tag = 'average'
                else:
                    tag = 'poor'
                
                self.tree.insert('', tk.END, values=(
                    int(row['id']),
                    row['name'],
                    row['email'],
                    row['category'],
                    f"{row['score']:.1%}",
                    f"{len(row['missing_skills'].split(',')) if row['missing_skills'] else 0} skills",
                    row['processed_date']
                ), tags=(tag,))
            
            self.status_var.set(f"Found {len(df)} matching applicants")
            
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {e}")
    
    def export_to_csv(self):
        """Export database to CSV"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                df = self.db_manager.get_all_applicants()
                df.to_csv(file_path, index=False)
                messagebox.showinfo("Success", f"Data exported to {Path(file_path).name}")
                self.status_var.set(f"Data exported to {Path(file_path).name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export data: {e}")
    
    def show_enhanced_statistics(self):
        """Show enhanced database statistics"""
        try:
            stats = self.db_manager.get_statistics()
            
            stats_window = tk.Toplevel(self.window)
            stats_window.title("Database Statistics")
            stats_window.geometry("500x400")
            stats_window.configure(bg=self.theme.colors['background'])
            
            # Header
            header_frame = ModernUIComponents.create_header(
                stats_window,
                "Database Statistics",
                "Analytics Overview"
            )
            header_frame.pack(fill='x', padx=20, pady=(15, 10))
            
            # Create cards for stats
            stats_container = ttk.Frame(stats_window)
            stats_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))
            
            # Total Applicants Card
            total_card = self.theme.create_card(stats_container)
            total_card.pack(fill='x', pady=(0, 15))
            
            ttk.Label(total_card, text="Total Applicants",
                     style='Subheading.TLabel').pack(pady=(15, 5))
            
            total_font = ('Segoe UI', 28, 'bold')
            total_label = tk.Label(total_card,
                                  text=str(stats['total_applicants']),
                                  font=total_font,
                                  fg=self.theme.colors['primary'],
                                  bg=self.theme.colors['card_bg'])
            total_label.pack(pady=(0, 15))
            
            # Average Score Card
            avg_card = self.theme.create_card(stats_container)
            avg_card.pack(fill='x', pady=(0, 15))
            
            ttk.Label(avg_card, text="Average Score",
                     style='Subheading.TLabel').pack(pady=(15, 5))
            
            avg_label = tk.Label(avg_card,
                                text=f"{stats['average_score']:.1%}",
                                font=total_font,
                                fg=self.theme.colors['success'],
                                bg=self.theme.colors['card_bg'])
            avg_label.pack(pady=(0, 15))
            
            # Categories Breakdown
            if stats['categories']:
                cat_frame = ttk.Frame(stats_container)
                cat_frame.pack(fill='both', expand=True)
                
                ttk.Label(cat_frame, text="Categories Breakdown",
                         style='Heading.TLabel').pack(anchor='w', pady=(0, 10))
                
                for cat_stat in stats['categories']:
                    cat_card = self.theme.create_card(cat_frame)
                    cat_card.pack(fill='x', pady=(0, 5))
                    
                    cat_content = ttk.Frame(cat_card)
                    cat_content.pack(fill='x', padx=15, pady=10)
                    
                    # Category name and count
                    name_frame = ttk.Frame(cat_content)
                    name_frame.pack(side='left', fill='y')
                    
                    ttk.Label(name_frame, text=cat_stat['category'],
                             style='Subheading.TLabel').pack(anchor='w')
                    ttk.Label(name_frame, text=f"{cat_stat['count']} applicants",
                             style='Body.TLabel').pack(anchor='w')
                    
                    # Score and progress
                    score_frame = ttk.Frame(cat_content)
                    score_frame.pack(side='right', fill='y')
                    
                    score_label = tk.Label(score_frame,
                                          text=f"{cat_stat['avg_score']:.1%}",
                                          font=('Segoe UI', 14, 'bold'),
                                          fg=self.theme.colors['text_primary'])
                    score_label.pack(anchor='e')
                    
                    # Progress bar
                    progress = ttk.Progressbar(score_frame,
                                              length=100,
                                              value=cat_stat['avg_score'] * 100)
                    progress.pack(anchor='e', pady=(5, 0))
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get statistics: {e}")


def main():
    root = tk.Tk()
    app = ResumeScreenerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()